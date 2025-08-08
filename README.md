# 定时报告ARH999指数
>这是一个定时向邮箱里发送ARH999指数的项目。
邮件中附有近一年BTC指数和ARH999指数的折线图，以及近一月ARH999指数、BTC指数、指数增长估值、200日定投成本的表格。
>
`fetch_arh999.fetch_arh999_data()`
一个获取ARH999指数的函数

`generate_arh999_table_html.generate_arh999_table_html()`
一个生成近一个月ARH999指数表格的函数

`visualize_arh999.generate_arh999_report_chart()`
一个生成近一个月ARH999指数图的函数

`send_arh999_report_email.send_arh999_report_email()`
一个负责发送email的函数

**项目中的ARH999指数来自`https://www.feixiaohao.com/data/ahrdata.html`**