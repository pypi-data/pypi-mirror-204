
import os
from .model import Model, get_optimizer, load_datas
from .model import get_label, get_train_test_data, get_device


def train(train_path: str, test_size: float = 0.1,
          encoding: str = "utf-8", split_data: str = "__",
          pretrained_model: str = "hfl/chinese-roberta-wwm-ext",
          learning_rate: float = 0.0001, optimizer: str = "adam",
          batch_size: int = 64, save_dir: str = "checkpoint",
          label_file_name: str = "catalog_label.txt", save_best: bool = False,
          max_length: int = 64, num_epochs: int = 25,
          device: str = "cuda:0", job_type: str = "txt_classification"):
    """
    :param train_path: 训练集数据，应该为txt文件
    :param test_size: 测试集比例，默认0.1
    :param encoding: 打开数据字符集，默认为utf-8
    :param split_data: 切分数据与标签的分隔符， 默认'__'
    :param pretrained_model: 预训练模型名称, 默认'hfl/chinese-roberta-wwm-ext'
    :param learning_rate: 学习率，默认0.000
    :param optimizer: 模型优化函数，默认adam
    :param batch_size: 训练批次大小，默认64，如果报错提示out of memory，可以适当调小
    :param save_dir: 训练checkpoint保存路径
    :param label_file_name: 保存标签文件名
    :param save_best: 是否只保存最优模型
    :param max_length: 默认序列最大长度64，超过部分会被自动截断
    :param num_epochs: 训练步数，默认25
    :param device: 训练设备。如果可用，默认使用第一块显卡
    :param job_type: 任务名称，保存模型开头名称，默认'txt_classification'
    :return: None
    """
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    if not os.path.exists(train_path):
        raise Exception(f"file:{train_path} does not exist.")
    print("开始读取数据")

    _device = get_device(device)

    datas = load_datas(train_path)

    print("读取数据完成")

    print("开始转换数据")
    (X_train, y_train), (X_test, y_test) = get_train_test_data(datas=datas, test_size=0.1)
    print("完成转换数据")
