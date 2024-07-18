import json
import random
import string
import uuid

def generate_random_number_key(length=11):  # 将长度改为11
    """生成指定长度的随机数字字符串，并加上下划线和另一个随机数字字符串"""
    part1 = ''.join(random.choices(string.digits, k=length))
    part2 = ''.join(random.choices(string.digits, k=6))  # 生成6位随机数字
    return f"{part1}_{part2}"


def update_json_file(file_path):
    """
    更新 JSON 文件中的 id, key, model 为随机值，并更新下级组件的 parentKey 与其直接上级组件的 key 一致。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 跳过第一个 id
    first_id_found = False

    def update_item(item, parent_key=None):
        nonlocal first_id_found

        if not first_id_found:
            first_id_found = True
        else:
            item['id'] = str(uuid.uuid4())

        new_key = generate_random_number_key()
        item['key'] = new_key
        item['model'] = f"{item['type']}_{new_key}"

        if 'parentKey' in item:
            item['parentKey'] = parent_key  # 更新 parentKey 为传入的上级 key

        # 如果是 grid 类型，递归处理其子组件
        if item['type'] == 'grid':
            for col in item['columns']:
                update_item(col, new_key)  # 将当前 grid 的 key 传递给子组件
                for sub_item in col.get('list', []):
                    update_item(sub_item, col['key'])  # 将 col 的 key 传递给子组件

    for item in data['list']:
        update_item(item)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    file_path = 'D:\\jj.json'  # 请替换为你的实际文件路径
    update_json_file(file_path)
    print('组件标识更新完成！')
