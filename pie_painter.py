from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import func


class Window(QMainWindow):
    def __init__(self, pie: dict):
        """
        方法，画出一个饼图。
        :param pie: {名称：值, }
        """
        super().__init__()

        self.setWindowTitle(func.ui["title"])
        self.setGeometry(550, 300, 800, 600)

        self.show()

        self.create_piechart(pie)

    def create_piechart(self, pie: dict):
        series = QPieSeries()
        for name, value in pie.items():
            series.append(name, value)

        # adding slice
        for slice in series.slices():
            slice.setLabelVisible(True)

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("单词查询计数")

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chartview)


def run(dic: dict):
    App = QApplication(sys.argv)
    window = Window(dic)
    return App.exec_()


# 测试代码
if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window(
        {
            "Python": 8000,
            "C++": 0,
            "Java": 0,
            "C#": 0,
            "PHP是最好的网页语言！": 1
        }
    )
    sys.exit(App.exec_())
