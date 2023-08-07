# -*- coding: utf-8 -*-
# @Time : 2023/3/31 13:50
# @Author : Zhan Yong
# @System : jk
import os
from pathlib import Path
import hashlib
import json
from tqdm import tqdm
import zipfile
from PIL import Image


class LabelmeLoad(object):

    def __init__(self, *args, **kwargs):
        self.parameter = args[0]
        self.group_error_path = ''
        self.out_of_bounds_path = ''
        self.error_path = ''

    def get_dir_currency(self):
        data_paths = []
        print(f'加载labelme数据集并封装数据结构')
        for root, dirs, files in tqdm(os.walk(self.parameter.input_datasets[0].get('input_dir'), topdown=True)):
            for file in files:
                path_name = os.path.join(root, file).replace('\\', '/')
                obj_path = Path(file)  # 初始化路径对象为对象
                if obj_path.suffix in self.parameter.file_formats:
                    # 所有labelme数据集存放规则为：图像必须存放在00.images目录中，图像对应的json文件必须存放在01.labelme中
                    if root.count('00.images') == 1:  # 设计规则，根据图片文件查找json文件，同时根据约定的目录规则封装labelme数据集
                        # print('字符串''中出现了1次')
                        relative_path = os.path.join('..', os.path.basename(root), file)
                        image_dir = root.replace(self.parameter.input_datasets[0].get('input_dir'), '').strip('\\/')
                        labelme_dir = os.path.join(image_dir.replace('00.images', '').strip('\\/'), '01.labelme')
                        labelme_file = obj_path.stem + '.json'
                        input_dir = self.parameter.input_datasets[0].get('input_dir')
                        json_path = os.path.join(input_dir, labelme_dir, labelme_file)
                        md5_value = self.get_md5_value(path_name)
                        if self.parameter.output_dir:  # 如果有输出路径，则自定义错误输出目录
                            self.group_error_path = os.path.join(self.parameter.output_dir, 'group_error_path')
                            self.out_of_bounds_path = os.path.join(self.parameter.output_dir, 'out_of_bounds_path')
                            self.error_path = os.path.join(self.parameter.output_dir, 'error_path')
                        image = Image.open(path_name)  # 通过PIL模块获取图像宽高
                        data_path = dict(image_dir=image_dir,  # 封装图像目录相对路径，方便后期路径重组及拼接
                                         image_file=file,  # 封装图像文件名称
                                         image_width=image.width,  # 封装图像宽度
                                         image_height=image.height,  # 封装图像高度
                                         labelme_dir=labelme_dir,  # 封装json文件相对目录
                                         labelme_file=labelme_file,  # 封装json文件名称
                                         input_dir=input_dir,  # 封装输入路径目录
                                         output_dir=self.parameter.output_dir,  # 封装输出路径目录
                                         group_error_path=self.group_error_path,  # 标注分组出错路径
                                         out_of_bounds_path=self.out_of_bounds_path,  # 标注超出图像边界错误路径
                                         error_path=self.error_path,  # 错误数据存放总目录，不分错误类别
                                         http_url=None,  # 封装http对象存储服务访问服务地址
                                         point_number=self.parameter.point_number,
                                         # 封装数据处理类型，包含base_labelme基类和coco基类
                                         data_type=self.parameter.input_datasets[0].get('type'),
                                         labelme_info=None,  # 封装一张图像标注属性信息
                                         background=False,  # 封装一张图像属于负样本还是正样本，默认为负样本即没有任何标注属性
                                         full_path=path_name,  # 封装一张图像绝对路径
                                         json_path=json_path,  # 封装一张图像对应json文件绝对路径
                                         md5_value=md5_value,  # 封装一张图像MD5值，用于唯一性判断
                                         relative_path=relative_path,
                                         # 封装图像使用标注工具读取相对路径，格式为：..\\00.images\\000000000419.jpg
                                         only_annotation=False, )  # 封装是图像还是处理图像对应标注内容的判断条件，默认图片和注释文件一起处理
                        labelme_info = self.load_labelme(data_path)  # 加载json内容
                        data_paths.append(labelme_info)
                    else:
                        print('文件夹目录不符合约定标准，请检查')
                        print(path_name)
        return data_paths

    @staticmethod
    def get_md5_value(path_name):
        """
        获取图像文件MD5值
        :param path_name:
        :return:
        """
        md5_obj = hashlib.md5()
        with open(path_name, 'rb') as f:
            while True:
                data = f.read(1024 * 1024)
                if not data:
                    break
                md5_obj.update(data)
        return md5_obj.hexdigest()

    @staticmethod
    def load_labelme(data_path):
        """
        获取图像文件对应的json文件内容
        :param data_path:
        :return:
        """
        # 组合加载json文件的路径
        labelme_path = os.path.join(data_path['input_dir'], data_path['labelme_dir'], data_path['labelme_file'])
        try:
            with open(labelme_path, 'r', encoding='UTF-8') as labelme_fp:
                data_path['labelme_info'] = json.load(labelme_fp)
                if data_path['labelme_info']['imageData'] is not None:
                    data_path['labelme_info']['imageData'] = None
                if not data_path['labelme_info']['shapes']:
                    data_path['background'] = True
        except Exception as e:
            # 如果没有json文件，读取就跳过，并设置为背景
            if 'No such file or directory' in e.args:
                data_path['background'] = True
                data_path['labelme_file'] = None
            else:  # 如果是其它情况错误（内容为空、格式错误），就删除json文件并打印错误信息
                print(e)
                print(labelme_path)
                # os.remove(labelme_path)
            data_path['background'] = True
        return data_path

    def compress_labelme(self):
        """
        封装压缩对象为字典，注意只对输入目录遍历一次，如果输入目录不对，封装结果就会出错
        :return:
        """
        print(f'封装压缩对象')
        for root, dirs, files in tqdm(os.walk(self.parameter.input_datasets[0].get('input_dir'), topdown=True)):
            zip_data = {}
            for directory in dirs:
                rebuild_input_dir = os.path.join(self.parameter.input_datasets[0].get('input_dir'), directory)
                zipfile_obj = os.path.join(self.parameter.output_dir, directory + '.zip')
                zip_data.update({rebuild_input_dir: zipfile_obj})
            return zip_data

    @staticmethod
    def make_compress(zip_package):
        """
        针对封装好的压缩目录进行迭代写入压缩对象包中
        该算法可以跨平台解压
        :param zip_package:
        """
        print(f'开始压缩')
        for zip_key, zip_value in tqdm(zip_package.items()):
            # zip_value：压缩包名称路径
            os.makedirs(os.path.dirname(zip_value), exist_ok=True)
            with zipfile.ZipFile(zip_value, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zip:  # 创建一个压缩文件对象
                for root, dirs, files in os.walk(zip_key):  # 递归遍历写入压缩文件到指定压缩文件对象中
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.join(os.path.basename(zip_key), os.path.relpath(file_path, zip_key))
                        # file_path：压缩文件绝对路径，relative_path：压缩文件相对路径，相对于压缩目录
                        zip.write(file_path, relative_path)

    @classmethod
    def get_videos_path(cls, root_dir, file_formats):
        """
        视频帧提取组合路径
        :param root_dir:
        :param file_formats:
        :return:
        """
        # dir_name_list = list()  # 文件夹名称
        # files_name = list()  # 文件名称
        # path_name = list()  # 文件夹路径
        file_path_name = list()  # 文件路径
        for root, dirs, files in os.walk(root_dir, topdown=True):
            dirs.sort()
            files.sort()
            # for dir_name in dirs:
            # if dir_name != '00.images' and dir_name != '01.labelme':
            # dir_name_list.append(dir_name)
            # 遍历文件名称列表
            for file in files:
                # 获取文件后缀
                file_suffix = os.path.splitext(file)[-1]
                # 如果读取的文件后缀，在指定的后缀列表中，则返回真继续往下执行
                if file_suffix in file_formats:
                    # 如果文件在文件列表中，则返回真继续往下执行
                    # files_name.append(file)
                    # path_name.append(root)
                    file_path_name.append(os.path.join(root, file))
        return file_path_name
