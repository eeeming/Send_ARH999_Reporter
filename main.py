import fetch_arh999
import generate_arh999_table_html
import visualize_arh999
import send_arh999_report_email

if __name__ == "__main__":
    print("开始生成 ARH999 报告...")
    
    # 1. 获取数据
    arh999_data = fetch_arh999.fetch_arh999_data()

    if arh999_data:
        # 2. 生成 HTML 表格
        generate_arh999_table_html.generate_arh999_table_html(arh999_data)

        # 3. 生成图表
        visualize_arh999.generate_arh999_report_chart(arh999_data)

        # 4. 发送邮件
        send_arh999_report_email.send_arh999_report_email()

        print("ARH999 报告生成和发送流程完成。")
    else:
        print("未能获取 ARH999 数据，报告生成流程终止。")

