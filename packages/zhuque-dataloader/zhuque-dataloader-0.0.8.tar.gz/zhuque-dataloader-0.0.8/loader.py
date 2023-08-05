"""
load zhuque graph
Args:
dataset_name: zhuque dataset name
data_loader: define data load param
algo_frame: algo frame, wholegraph/grapscope etc.
"""
# -*- coding:utf-8 -*-
import os.path
import yaml




LOCAL_DATASET_PATH = '/INPUT/datasets/'
LOCAL_DATALOADER_PATH = '/INPUT/dataloaders/'
OGB_LOAD_MAP = {
    ('pyg', 'node'): 'PygNodePropPredDataset',
    ('pyg', 'link'): 'PygLinkPropPredDataset',
    ('pyg', 'graph'): 'PygGraphPropPredDataset',
    ('dgl', 'node'): 'DglNodePropPredDataset',
    ('dgl', 'link'): 'DglLinkPropPredDataset',
    ('dgl', 'graph'): 'DglGraphPropPredDataset',
    ('none', 'node'): 'NodePropPredDataset',
    ('none', 'link'): 'LinkPropPredDataset',
    ('none', 'graph'): 'GraphPropPredDataset'
}
OGB_GS_LOAD_MAP = {
    'ogbl_collab': 'load_ogbl_collab',
    'ogbl_ddi': 'load_ogbl_ddi',
    'ogbn_arxiv': 'load_ogbn_arxiv',
    'ogbn_mag_small': 'load_ogbn_mag',
    'ogbn_proteins': 'load_ogbn_proteins'
}
NAS_BASE = '/mnt/zhuque_goofys'
k8s_volumes = {
    "data": {
        "type": "hostPath",
        "field": {
            "path": NAS_BASE,
            "type": "Directory"
        },
        "mounts": {
            "mountPath": "/zhuque_goofys"
        }
    }
}


def load_graph(args):
    data_name = args.data_name
    data_loader = args.data_loader
    frame_type = args.frame_type
    if not data_name or not data_loader or not frame_type:
        raise Exception('please check dataset parameters')
    dataloader_path = os.path.join(LOCAL_DATALOADER_PATH, data_loader + '.yml')
    try:
        dl_file = open(dataloader_path, "r", encoding="UTF-8")
        dataloader = yaml.load(dl_file, Loader=yaml.FullLoader)
    except:
        raise Exception('read dataloader file error')

    # 检测dataloader文件字段是否存在
    if 'storageFormat' not in dataloader.keys():
        raise Exception('check the dataloader, storageFormat does not exsits')
    storage_format = dataloader['storageFormat']
    if storage_format in ['csv', 'ogb'] and 'platform' not in dataloader.keys():
        raise Exception('check the dataloader, platform does not exsits')

    # 朱雀平台格式csv数据集
    if storage_format == 'csv':
        platform = dataloader['platform']
        if platform == 'graphscope':
            return load_graph_csv_gs(data_name, dataloader)
        elif platform == 'wholegraph':
            return load_graph_wg(data_name)
    elif storage_format == 'ogb':
        platform = dataloader['platform']
        if platform == 'ogbofficial':
            return load_graph_ogb_official(dataloader, frame_type)
        elif platform == 'wholegraph':
            return load_graph_wg(data_name)
        elif platform == 'graphscope':
            return load_graph_ogb_gs(data_name, dataloader)
    elif storage_format in ('npy', 'npz'):
        return load_graph_numpy(dataloader)
    elif storage_format == 'other':
        return load_graph_other(dataloader, args.data_path)

    raise Exception('load data fail')



# 加载ogb格式数据集 官方方式
def load_graph_ogb_official(dataloader, frame_type):
    from ogb.graphproppred import PygGraphPropPredDataset, DglGraphPropPredDataset, GraphPropPredDataset
    from ogb.linkproppred import PygLinkPropPredDataset, DglLinkPropPredDataset, LinkPropPredDataset
    from ogb.nodeproppred import PygNodePropPredDataset, DglNodePropPredDataset, NodePropPredDataset

    ogb_name = dataloader['ogbName']
    ogb_root = dataloader['ogbRoot']
    task = get_ogb_task(ogb_name)
    params = []
    normal_ogb_name = ogb_name.replace("_", "-")
    params.append('name=\'' + normal_ogb_name + '\'')
    params.append('root=\'' + ogb_root + '\'')
    # obj_str : PygNodePropPredDataset(name='ogbl-ddi', root=data_path)
    data_frame = get_data_frame(frame_type)
    obj_str = OGB_LOAD_MAP.get((data_frame, task)) + construct_param(params)
    print(obj_str)
    return eval(obj_str)


# 加载ogb格式数据集 在wholegraph框架
def load_graph_ogb_wg(dataloader):
    from wg_torch.graph_ops import (
        graph_name_normalize,load_meta_file,load_pickle_data
    )
    from gnn.gnn_homograph_data_preprocess import download_and_convert_node_classification
    from gnn.gnn_homograph_data_preprocess import download_and_convert_link_prediction
    from gnn.gnn_homograph_data_preprocess import build_homo_graph
    from zhuque_graph.dataloader.wholegraph.homograph_data_convert_node_classification import homograph_data_convert_node_classification
    from zhuque_graph.dataloader.wholegraph.homograph_data_convert_link_prediction import homograph_data_convert_link_prediction
    from ogb.graphproppred import PygGraphPropPredDataset, DglGraphPropPredDataset, GraphPropPredDataset
    from ogb.linkproppred import PygLinkPropPredDataset, DglLinkPropPredDataset, LinkPropPredDataset
    from ogb.nodeproppred import PygNodePropPredDataset, DglNodePropPredDataset, NodePropPredDataset


    ogb_name = dataloader['ogbName']
    ogb_root = dataloader['ogbRoot']
    task = get_ogb_task(ogb_name)
    normal_graph_name = graph_name_normalize(ogb_name)
    root_dir = os.path.join(ogb_root, normal_graph_name)
    output_dir = os.path.join(ogb_root, normal_graph_name, "converted")

    if task == 'node':
        download_and_convert_node_classification(output_dir, ogb_root, ogb_name)
    elif task == 'link':
        download_and_convert_link_prediction(output_dir, ogb_root, ogb_name)
    else:
        raise Exception('task not supported')

    train_data, valid_data, test_data = load_pickle_data(ogb_root, normal_graph_name, True)
    return train_data, valid_data, test_data


# 加载ogb格式数据集 在graphscope框架
def load_graph_ogb_gs(data_name, dataloader):
    import graphscope as gs
    from graphscope.dataset.ogbl_collab import load_ogbl_collab
    from graphscope.dataset.ogbl_ddi import load_ogbl_ddi
    from graphscope.dataset.ogbn_arxiv import load_ogbn_arxiv
    from graphscope.dataset.ogbn_mag import load_ogbn_mag
    from graphscope.dataset.ogbn_proteins import load_ogbn_proteins


    sess = None
    ogb_name = dataloader['ogbName']
    normal_ogb_name = ogb_name.replace("-", "_")
    if normal_ogb_name not in OGB_GS_LOAD_MAP.keys():
        raise Exception(normal_ogb_name + ' is not supported in GraphScope,\n'
                       'supported list contains: \nogbl_collab\nogbl_ddi \nogbn_arxiv\nogbn_mag\nogbn_proteins\n')
    try:
        sess = gs.session(addr='127.0.0.1:59001', mount_dataset='/dataset')
        print(sess)
        params = []
        params.append('sess')
        params.append('\'/FILES/INPUT/' + data_name + '\'')
        obj_str = OGB_GS_LOAD_MAP.get(normal_ogb_name) + construct_param(params)
        # graph = load_ogbn_mag(sess, '/FILES/INPUT/ogbn_mag_small')
        print(obj_str)
        return eval(obj_str)
    except:
        print('load ogb graph in GraphScope error')
        raise Exception('load ogb graph in GraphScope error')
    finally:
        sess.close()



# 加载numpy格式数据集
def load_graph_numpy(dataloader):
    params = dataloader['params']
    obj_str = 'np.load' + construct_param(params)
    print(obj_str)
    return eval(obj_str)


# 加载other格式数据集
def load_graph_other(dataloader, data_path):
    code = dataloader['code']
    print(code)
    exec_data = {}
    exec(code, globals(), exec_data)
    return exec_data["data"]


# 加载csv格式数据集在graphscope框架
def load_graph_csv_gs(data_name, dataloader):
    import graphscope
    # from graphscope.dataset import *

    data_path = os.path.join(LOCAL_DATASET_PATH, data_name)
    sess = graphscope.session(mount_dataset="/dataset", k8s_volumes=k8s_volumes, k8s_coordinator_cpu=4,
                              k8s_coordinator_mem="8Gi")
    if dataloader["oidType"] == 'string':
        graph = sess.g(oid_type=dataloader["oidType"])
    else:
        graph = sess.g()
    for key, value in dataloader['vertices'].items():
        pro = []
        for feature in value['features']:
            pro.append((feature['name'], feature['type']))
        graph = graph.add_vertices(os.path.join(data_path, value['path']), label=key, vid_field=value['vidField'],
                                   properties=pro)
    for key, value in dataloader['edges'].items():
        pro = []
        for feature in value['features']:
            pro.append((feature['name'], feature['type']))
        graph = graph.add_edges(os.path.join(data_path, value['path']), label=key, src_label=value['srcLabel'],
                                dst_label=value['dstLabel'], src_field=0, dst_field=1, properties=pro)
    return graph

def load_graph_csv_wg_old(data_name, dataloader):
    from wg_torch.graph_ops import (
        graph_name_normalize, load_pickle_data
    )
    from zhuque_graph.dataloader.wholegraph.homograph_data_convert_node_classification import \
        homograph_data_convert_node_classification
    from zhuque_graph.dataloader.wholegraph.homograph_data_convert_link_prediction import \
        homograph_data_convert_link_prediction

    task = dataloader['task']
    data_path = os.path.join(LOCAL_DATASET_PATH, data_name)
    if not task or not data_name:
        raise Exception('please check task or dataset name')
    node_name = ''
    node_file = ''
    edge_name = ''
    edge_file = ''
    for key, value in dataloader['vertices'].items():
        node_name = key
        node_file = os.path.join(data_path, value['path'])
        break
    for key, value in dataloader['edges'].items():
        edge_name = key
        edge_file = os.path.join(data_path, value['path'])
        break
    normal_graph_name = graph_name_normalize(data_name)
    if task == 'node_classification':
        homograph_data_convert_node_classification(
            os.path.join(LOCAL_DATASET_PATH, data_name, "converted"),
            node_file,
            edge_file,
            normal_graph_name,
            node_name,
            edge_name
        )
    elif task == 'link_prediction':
        homograph_data_convert_link_prediction(
            os.path.join(LOCAL_DATASET_PATH, data_name, "converted"),
            node_file,
            edge_file,
            normal_graph_name,
            node_name,
            edge_name
        )
    else:
        raise Exception('task not supported')

    train_data, valid_data, test_data = load_pickle_data(LOCAL_DATASET_PATH, data_name, True)
    return train_data, valid_data, test_data


def load_graph_wg(data_name):
    from wg_torch.graph_ops import (
        graph_name_normalize, load_pickle_data, HomoGraph
    )
    from wg_torch.wm_tensor import (
        create_intra_node_communicator, create_global_communicator
    )
    from wholegraph.torch import wholegraph_pytorch as wg
    import torch
    from mpi4py import MPI

    wg.init_lib()
    torch.set_num_threads(1)
    comma = MPI.COMM_WORLD
    shared_comma = comma.Split_type(MPI.COMM_TYPE_SHARED)
    os.environ["RANK"] = str(comma.Get_rank())
    os.environ["WORLD_SIZE"] = str(comma.Get_size())
    # slurm in Selene has MASTER_ADDR env
    if "MASTER_ADDR" not in os.environ:
        os.environ["MASTER_ADDR"] = "localhost"
    if "MASTER_PORT" not in os.environ:
        os.environ["MASTER_PORT"] = "12335"
    local_rank = shared_comma.Get_rank()
    local_size = shared_comma.Get_size()

    print("Rank=%d, local_rank=%d" % (local_rank, comma.Get_rank()))
    dev_count = torch.cuda.device_count()
    assert dev_count > 0
    assert local_size <= dev_count
    torch.cuda.set_device(local_rank)
    torch.distributed.init_process_group(backend="nccl", init_method="env://")
    wm_comm = create_intra_node_communicator(
        comma.Get_rank(), comma.Get_size(), local_size
    )
    wm_embedding_comm = None
    use_nccl = True # options.use_nccl: set True temporarily
    if use_nccl:
        if comma.Get_rank() == 0:
            print("Using nccl embeddings.")
        wm_embedding_comm = create_global_communicator(
            comma.Get_rank(), comma.Get_size()
        )
    # if comma.Get_rank() == 0:
    #     print("Framework=%s, Model=%s" % (options.framework, options.model))

    train_data, valid_data, test_data = load_pickle_data(LOCAL_DATASET_PATH, data_name, True)

    dist_homo_graph = HomoGraph()
    use_chunked = True
    use_host_memory = False
    dist_homo_graph.load(
        LOCAL_DATASET_PATH,
        data_name,
        wm_comm,
        use_chunked,
        use_host_memory,
        wm_embedding_comm,
    )
    print("Rank=%d, Graph loaded." % (comma.Get_rank(),))

    return train_data, valid_data, test_data, dist_homo_graph


# 判断ogb数据集的任务类型
def get_ogb_task(data_name):
    if 'ogbn' in data_name:
        return 'node'
    elif 'ogbl' in data_name:
        return 'link'
    elif 'ogbg' in data_name:
        return 'graph'
    else:
        raise Exception('dataset name is invalid')


# 组装参数
def construct_param(params):
    param_str = ''
    for param in params:
        param_str = param_str + ',' + param
    if len(param_str) > 0:
        param_str = param_str[1:]
    param_str = '(' + param_str + ')'
    return param_str

def get_data_frame(frame_type):
    if frame_type == 'pytorch':
        return 'pyg'
    elif frame_type == 'dgl':
        return 'dgl'
    else:
        return 'none'

