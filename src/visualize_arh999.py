import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates # 用于更好地处理日期轴
from datetime import timedelta
import logging

# 确保中文字符能够正常显示
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei'] # 使用你通过 fc-list 找到的字体名称
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

def generate_arh999_report_chart(data, output_path="arh999_report_chart.png"):
    """
    绘制包含ARH999指数、BTC全球指数、定投区间及当前值的报告图表。
    :param data: 包含ARH999指数及相关数据的列表
    :param output_path: 图片保存路径和文件名
    """
    
    # 1. 数据准备
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date').reset_index(drop=True)

    end_date = df['date'].max()
    start_date = end_date - timedelta(days=365) # 近一年，可以调整天数
    plot_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # 获取近一年数据
    dates = plot_df['date']
    arh999_values = plot_df['arh999']
    btc_global_index_values = plot_df['btc_global_index']
    
    # 获取最新数据用于文本显示
    latest_arh999 = arh999_values.iloc[-1]
    # 2. 创建图表和主副坐标轴
    fig, ax1 = plt.subplots(figsize=(14, 7)) # 创建图表和主Y轴
    
    # 主Y轴：ARH999 指数
    ax1.set_xlabel('日期', fontsize=12)
    ax1.set_ylabel('ARH999 指数', color='red', fontsize=12)
    ax1.plot(dates, arh999_values, linestyle=':', color='red', label='ARH999 指数')
    ax1.tick_params(axis='y', labelcolor='red')
    ax1.grid(True, linestyle='--', alpha=0.7) 
    ax1.set_ylim(0, 2.5) # 假设ARH999的正常波动范围在0到30之间，你可以根据实际数据调整
    # 3. 添加定投区间水平线和填充
    lower_bound = 0.45
    upper_bound = 1.2
    ax1.axhline(lower_bound, color='green', linestyle='--', linewidth=1.5, label=f'定投下限 ({lower_bound})')
    ax1.axhline(upper_bound, color='red', linestyle='--', linewidth=1.5, label=f'定投上限 ({upper_bound})')
    ax1.axhspan(lower_bound, upper_bound, color='palegreen', alpha=0.3, label='理论定投区间') # 填充区间
    # 4. 创建副坐标轴：BTC 全球指数
    ax2 = ax1.twinx() # 创建共享X轴的副Y轴
    ax2.set_ylabel('BTC 全球指数', color='blue', fontsize=12)
    ax2.plot(dates, btc_global_index_values, linestyle='-', color='blue', label='BTC 全球指数')
    ax2.tick_params(axis='y', labelcolor='blue')
    # 5. 设置X轴日期格式
    # 自动选择合适的日期刻度间隔
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45) # 日期标签旋转45度
    if not dates.empty: # 避免数据为空时报错
        ax1.set_xlim(dates.iloc[0], dates.iloc[-1]) # 将X轴范围设置为数据的最小日期和最大日期
    # 6. 添加图表标题和图例
    # plt.title('ARH999 指数与 BTC 全球指数趋势', fontsize=18)
    
    # 合并两个轴的图例
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left', bbox_to_anchor=(1.07, 1)) # 将图例放在图表外部右上方
    # 7. 添加自定义文本（当前指标和定投区间）
    # 调整文本位置，可以根据图表大小和实际效果调整xy坐标
    fig.text(1.05, 0.18, f'当前ARH999指标: {latest_arh999:.4f}', 
             transform=ax2.transAxes, fontsize=12, verticalalignment='top', 
             bbox=dict(boxstyle='round,pad=0.5', fc='white', ec='gray', lw=0.5))
    fig.text(1.05, 0.08, '理论定投区间: 0.45-1.2', 
             transform=ax2.transAxes, fontsize=12, verticalalignment='top', 
             bbox=dict(boxstyle='round,pad=0.5', fc='white', ec='gray', lw=0.5))
    plt.tight_layout(rect=[0, 0, 0.9, 1]) # 自动调整布局，为图例和文本留出空间
    
    # 8. 保存图表
    plt.savefig(output_path, dpi=300, bbox_inches='tight') # dpi提高分辨率，bbox_inches='tight'确保所有元素都被保存
    plt.close(fig) # 关闭图表，释放内存
    logging.info(f"ARH999 报告图表已保存到: {output_path}")

    # 集成到 main 模块 (如果你选择这样做的话)
if __name__ == "__main__":
    from fetch_arh999 import fetch_arh999_data # 导入我们第一步的函数
    
    arh999_full_data = fetch_arh999_data()
    if arh999_full_data:
        logging.info("已获取所有 ARH999 历史数据，开始生成图表...")
        # 调用新的图表生成函数
        generate_arh999_report_chart(arh999_full_data, output_path="arh999_report_chart.png")
        logging.info("图表生成完成。")
    else:
        logging.warning("未能获取 ARH999 数据，跳过图表生成。")