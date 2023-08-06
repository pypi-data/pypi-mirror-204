import yaml

def oss_info():
    # 读取yaml文件
    with open('/Users/lihaijian/.lhj/oss_config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # 输出
    return config
