import pandas as pd
from datetime import timedelta # 确保导入 timedelta
from fetch_arh999 import fetch_arh999_data
import logging
# 假设 data 是你从 fetch_arh999_data() 获取到的数据
# data = fetch_arh999_data() # 你在实际运行中需要调用这个函数来获取数据

def generate_arh999_table_html(data, output_path="arh999_report_table.html"):
    """
    生成包含ARH999相关数据的HTML表格。
    :param data: 包含ARH999指数及相关数据的列表 (从 fetch_arh999_data 获取)
    :param output_path: HTML文件保存路径和文件名
    """
    if data is None:
        logging.warning("没有数据可以生成表格。")
        return

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date').reset_index(drop=True)

    # 筛选出最近30天的数据
    end_date = df['date'].max()
    start_date = end_date - timedelta(days=30) # 近30天
    table_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    table_df = table_df.sort_values(by='date', ascending=False).reset_index(drop=True)

    html_string = """
    <table border="1" style="width:100%; border-collapse: collapse; text-align:center;">
        <thead>
            <tr style="background-color:#f2f2f2;">
                <th style="padding: 8px;">日期</th>
                <th style="padding: 8px;">ARH999 指数</th>
                <th style="padding: 8px;">BTC 全球指数</th>
                <th style="padding: 8px;">指数增长估值</th>
                <th style="padding: 8px;">200日定投成本</th>
            </tr>
        </thead>
        <tbody>
    """

    # 循环遍历 table_df 中的每一行数据，生成表格的行
    for index, row in table_df.iterrows():
        # 获取每一列的数据
        date = row['date'].strftime('%Y-%m-%d') # 将日期格式化为字符串
        arh999 = f"{row['arh999']:.4f}" # 格式化浮点数，保留4位小数
        btc_global_index = f"{row['btc_global_index']:.2f}" # 保留2位小数
        growth_estimation = f"{row['growth_estimation']:.2f}"
        daily_investment_cost_200d = f"{row['daily_investment_cost_200d']:.2f}"
        
        # 构建当前行的 HTML 字符串
        html_string += f"""
            <tr>
                <td style="padding: 8px;">{date}</td>
                <td style="padding: 8px;">{arh999}</td>
                <td style="padding: 8px;">{btc_global_index}</td>
                <td style="padding: 8px;">{growth_estimation}</td>
                <td style="padding: 8px;">{daily_investment_cost_200d}</td>
            </tr>
        """
    
    # 结束 <tbody> 和 <table> 标签
    html_string += """
        </tbody>
    </table>
    """

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_string)
    logging.info(f"ARH999 报告表格已保存到: {output_path}")

# 示例调用 (假设你已经有了 data)
# generate_arh999_table_html(your_fetched_data_variable)

if __name__ == "__main__":
    data = fetch_arh999_data()
    generate_arh999_table_html(data)