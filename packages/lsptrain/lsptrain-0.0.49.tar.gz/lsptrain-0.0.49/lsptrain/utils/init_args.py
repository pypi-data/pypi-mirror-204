# encoding: utf-8

import argparse


def setup_classification_args():
    parser = argparse.ArgumentParser("预训练分类任务")
    parser.add_argument("--train_path", type=str,
                        help="训练集数据，应该为txt文件")
    parser.add_argument("--test_size", default=0.1, type=float,
                        help="测试集比例，默认0.1")
    parser.add_argument("--encoding", default="utf-8", type=str,
                        help="打开数据字符集，默认为utf-8")
    parser.add_argument("--split_data", default="__", type=str,
                        help="切分数据与标签的分隔符， 默认'__'")
    parser.add_argument("-pm", "--pretrained_model", default="hfl/chinese-roberta-wwm-ext", type=str,
                        help="预训练模型名称, 默认'hfl/chinese-roberta-wwm-ext'")
    parser.add_argument("-lr", "--learning_rate", default=0.0001,
                        type=float, help="学习率，默认0.0001")
    parser.add_argument("-o", "--optimizer", choices=["adam", "sgd"], default="adam", type=str,
                        help="模型优化函数，默认adam")
    parser.add_argument("-b", "--batch_size", default=64, type=int,
                        help="训练批次大小，如果报错提示out of memory，可以适当调小")
    parser.add_argument("-s", "--save_dir", default="checkpoint", type=str,
                        help="训练checkpoint保存路径")
    parser.add_argument("--label_file_name", default="catalog_label.txt", type=str,
                        help="保存标签文件名")
    parser.add_argument("--save_best", default=False, type=bool,
                        help="是否只保存最优模型")
    parser.add_argument("--max_length", default=64, type=int,
                        help="默认序列最大长度64，超过部分会被自动截断")
    parser.add_argument("-e", "--num_epochs", default=25, type=int,
                        help="训练步数，默认25")
    parser.add_argument("-d", "--device", default="cuda:0",
                        help="训练设备。如果可用，默认使用第一块显卡")
    parser.add_argument("-j", "--job_type", default="txt_classification", type=str,
                        help="任务名称，保存模型开头名称，默认'txt_classification'")
    args = parser.parse_args()

    return args
