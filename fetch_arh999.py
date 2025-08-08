import requests
import datetime

def fetch_arh999_data():
    """
    从API获取ARH999指数数据。
    """
    url = 'https://dncapi.flink1.com/api/v2/index/arh999?code=bitcoin&webp=1'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'origin': 'https://www.feixiaohaometa.com',
        'referer': 'https://www.feixiaohaometa.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
        # 你可以根据需要添加 curl 命令中其他的 headers，通常 'User-Agent' 和 'Referer' 比较重要
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # 检查HTTP请求是否成功 (2xx 状态码)
        data = response.json()
        
        # API返回的数据结构可能是 {'data': [[...], [...], ...]} 或者直接是 [[...], [...], ...]
        # 根据你提供的示例，看起来直接就是列表，但保险起见，我们可以检查一下
        if isinstance(data, dict) and 'data' in data:
            arh999_raw_data = data['data']
        else:
            arh999_raw_data = data
            
        cleaned_data = []
        for item in arh999_raw_data:
    # 确保数据结构符合预期，至少有5个元素
            if len(item) >= 5: 
                timestamp = item[0]
                arh999_value = item[1]
                btc_global_index = item[2] # 新增
                growth_estimation = item[3] # 新增
                daily_investment_cost_200d = item[4] # 新增
                
                dt_object = datetime.datetime.fromtimestamp(timestamp)
                
                cleaned_data.append({
                    'date': dt_object.strftime('%Y-%m-%d'), 
                    'arh999': float(arh999_value),
                    'btc_global_index': float(btc_global_index), # 确保是浮点数
                    'growth_estimation': float(growth_estimation), # 确保是浮点数
                    'daily_investment_cost_200d': float(daily_investment_cost_200d) # 确保是浮点数
                })
        
        # 接下来，我们需要筛选出近30天的数据
        # 提示：你可以先将所有数据按日期排序（如果API返回的不是有序的），然后取最后30条。
        # 或者，如果API返回的是最新数据在前，直接取前30条。
        # 如果需要基于日期判断，你可以计算出30天前的日期，然后过滤。
        
        # 这里先简单返回所有清洗后的数据，筛选30天的逻辑可以后面再加
        return cleaned_data
        
    except requests.exceptions.RequestException as e:
        print(f"请求API失败: {e}")
        return None
    except ValueError as e:
        print(f"解析JSON失败或数据格式不正确: {e}")
        return None

if __name__ == "__main__":
    arh999_data = fetch_arh999_data()
    if arh999_data:
        # 打印最新几条数据看看效果
        print("最新几条 ARH999 数据：")
        for entry in arh999_data[-5:]: # 打印最后5条
            print(f"日期: {entry['date']}, "
                  f"ARH999 指数: {entry['arh999']:.4f}, "
                  f"BTC全球指数: {entry['btc_global_index']:.2f}, "
                  f"指数增长估值: {entry['growth_estimation']:.2f}, "
                  f"200日定投成本: {entry['daily_investment_cost_200d']:.2f}")
