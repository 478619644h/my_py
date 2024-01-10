#coding=utf-8

from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts import options as opts
from datahandle.dbopration import DB

with DB() as db:
   time = []
   ali_pay = []
   chat_pay = []
   baitiao = []
   total = []
   db.execute("select * from statistics  ORDER BY pay_time")
   for data in db.fetchall():
        time.append(data["pay_time"])
        ali_pay.append(data["ali_pay"])
        chat_pay.append(data["chat_pay"])
        baitiao.append(data["jd_baitiao_pay"])
        total.append(data["total"])
   bar = (
       Bar()
       .add_xaxis(time)
       .add_yaxis(u"花呗", ali_pay)
       .add_yaxis(u"微信", chat_pay)
       .add_yaxis(u"白条", baitiao)
       .add_yaxis(u"总计", total)
       .set_global_opts(title_opts=opts.TitleOpts(title=u"每月花费"))
   )
   bar.render("bar_statistics.html")
   line = (
           Line()
            .add_xaxis(time)
            .add_yaxis(
               "花呗",
               ali_pay,
               label_opts=opts.LabelOpts(is_show=False),
               markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]))
            .add_yaxis("微信",
                       chat_pay,
                       label_opts=opts.LabelOpts(is_show=False),
                        markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                       )
            .add_yaxis("白条", baitiao,label_opts=opts.LabelOpts(is_show=False),
                       markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
                       )
            .add_yaxis("总计", total,label_opts=opts.LabelOpts(is_show=False),
                       markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),)
            .set_global_opts(
                   title_opts=opts.TitleOpts(title="每月花费"),
                   tooltip_opts=opts.TooltipOpts(trigger="axis"),
                   yaxis_opts=opts.AxisOpts(
                       type_="value",
                       axistick_opts=opts.AxisTickOpts(is_show=True),
                       splitline_opts=opts.SplitLineOpts(is_show=True)
               ),
               xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            )
   )
   line.render("line_statistics.html")