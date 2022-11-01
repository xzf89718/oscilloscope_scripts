# Author: Zifeng Xu
# Email: zifeng.xu@foxmail.com
# Usage: Provide a full python analysis skeleton to analyze the data which taken from the cosmic ray muon detection experiment
# Dependencies: python 3.6+, numpy matplotlib pandas
# 怎么做? 先编辑脚本，编写自己的分析
# 1, 从QuickAnalysisBase派生一个子类，重写Begin(), Process(), Terminate()这三个函数
# 2, 在Begin()内，使用self.BookAnalysis("name_of_analysis"), 登记你要做的分析
# 3, 在Process()内，对读取的数据进行分析。当前读取到的文件的时间存在：self.scaled_time[channel]内；读取到的文件的电压存在：self.scaled_voltage[channel]内，数据格式为numpy的ndarray。
# 对数据进行分析，然后调用self.Fill("name_of_analysis", value), 将分析所得值储存在self.analysis_result["name_of_analysis"]内
# 4, 在Terminate()内，对分析得到的结果进行可视化。我准备了self.QuickHist()和self.QuickResult()供同学们调用，可以快速画柱状图和均值，中位数，实验标准差
# 5, 在本脚本的最下方，加入：
# quickanalysis=QuickAnalysis_Zifeng(INPUT_FILENAME, N_SAVE_WAVEFORMS, SAVE_CHANNELS, INPUT_DIR)
# quickanalysis.RunAnalysis()
# 提醒：可以直接修改助教这里写的QuickAnalysis_Zifeng() (类名改下。。。。)
# 提醒：要修改柱状图的格式，可以修改QuickAnalysisBase中的QuickHist(), 更好的做法是，在自己的派生类中重写一个，仿照基类
# 提醒：要修改分析的结果，可以修改QuickAnalysisBase中的QuickResult(), 更好的做法是，在自己的派生类中重写一个，仿照基类
# 运行分析
# Example：python QuickAnalysis.py this_is_an_example --n_save_waveforms 10 --save_channels CH1,CH2 --input_dir input_dir
import argparse
import os

# In order to use ndarray
import numpy as np
# In order to read data from csv
import pandas as pd
# In order to make simple histograms
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# Analysis Base class


class QuickAnalysisBase(object):

    def __init__(self, input_fileprefix, n_save_waveforms, save_channels, input_dir, data_length=2000, begin_entry=0):
        # Read from user
        self.input_fileprefix = input_fileprefix
        self.n_save_waveforms = n_save_waveforms
        self.save_channels = save_channels.split(",")
        self.input_dir = input_dir
        self.data_length = data_length
        self.begin_entry = begin_entry

        # Use in QuickAnalysis
        self.entry = None
        self.scaled_time = {}
        self.scaled_voltage = {}
        self.analysis_result = {}

        # Just a container to hold data in each entry
        self.dataframe = {}

    def Print(self, option=""):
        print("QuickAnalysisBase Print:")
        print("Arguments set by user:\nintput_fileprefix\tn_save_waveforms\tsave_channels\tinput_dir\tdata_length\tbegin_entry\n{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(
            self.input_fileprefix, self.n_save_waveforms, self.save_channels, self.input_dir, self.data_length, self.begin_entry))
        print("Variables calculate by QuickAnalysis:")
        print("entry\n{0}\nscaled_time\n{1}\nscaled_voltage\n{2}\nanalysis_result\n{3}".format(
            self.entry, self.scaled_time, self.scaled_voltage, self.analysis_result))

        return True

    def BookAnalysis(self, analysis_name):
        self.analysis_result[analysis_name] = []

        return True

    def Fill(self, analysis_name, value):
        self.analysis_result[analysis_name].append(value)

        return True

    def LoadData(self):
        for channel in self.save_channels:
            data_dir = "{0}-{1}-{2}.csv".format(
                self.input_fileprefix, channel, self.entry)
            self.dataframe[channel] = pd.read_csv(os.path.join(
                self.input_dir, data_dir), sep=",")
            self.scaled_time[channel] = self.dataframe[channel]['scaled_time']
            self.scaled_voltage[channel] = self.dataframe[channel]["scaled_voltage"]
            print("Load data from:{0}".format(data_dir))

        return True

    def DeleteOneData(self):
        for channel in self.save_channels:
            del self.dataframe[channel]
        return True

    def Initialize(self):

        self.entry = self.begin_entry
        for channel in self.save_channels:
            # Assume dtype is float
            self.scaled_time[channel] = np.zeros(
                self.data_length, dtype=float)
            self.scaled_voltage[channel] = np.zeros(
                self.data_length, dtype=float)
            self.dataframe[channel] = None
        self.Print()
        return True
    # Need to rewrite in the child class Begin(), Process(), Terminate()

    def Begin(self):
        pass

    def Process(self):
        pass

    def Terminate(self):
        pass

    def QuickHist(self):
        NUM_BINS = 100
        # In this QuickHist method, plot simple histogram for every analysis
        for ana in self.analysis_result.keys():
            print("Make histogram for {0}".format(ana))
            fig, ax = plt.subplots()
            n, bins, patches = ax.hist(
                self.analysis_result[ana], bins=NUM_BINS, density=False)
            ax.set_title(
                "THIS PLOT MADE BY ZIFENG. MODIFY IT BEFORE SUBMIT YOUR REPORT!!!!")
            ax.set_xlabel(ana)
            ax.set_ylabel("Number of events")
            fig.savefig("{0}_QuickHistplot.png".format(ana))

        return True

    def QuickResult(self):
        # Only calculate some simple quantity
        for ana in self.analysis_result.keys():
            print("Make result for {0}".format(ana))
            mean = np.mean(self.analysis_result[ana])
            median = np.median(self.analysis_result[ana])
            std = np.std(self.analysis_result[ana], ddof=1)
            print("mean\tmedian\tstd error\n{0}\t{1}\t{2}".format(
                mean, median, std))

        return True

    def QuickPlot(self):
        # Only call during Process()
        fig, ax = plt.subplots()
        for channel in self.save_channels:
            ax.plot(self.scaled_time[channel], self.scaled_voltage[channel])
        ax.set_title(
            "THIS PLOT MADE BY ZIFENG. MODIFY IT BEFORE SUBMIT YOUR REPORT!!!!")
        ax.set_xlabel("scaled_time/s")
        ax.set_ylabel("scaled_voltage/V")
        channels = self.save_channels[0]
        for channel in self.save_channels[1:]:
            channels = channels+"_"+channel
        fig.savefig(
            "{0}-{1}-{2}.png".format(self.input_fileprefix, channels, self.entry))

        return True

    def Loop(self):
        while self.entry < self.n_save_waveforms:
            self.LoadData()
            self.Process()
            self.DeleteOneData()
            self.entry = self.entry + 1

        return True

    def RunAnalysis(self):
        self.Initialize()
        self.Begin()
        self.Loop()
        self.Terminate()

        return True

# If you want an example


class QuickAnalysis_Zifeng(QuickAnalysisBase):

    """
    This is an example on How-to use QuickAnalysis
    """

    def __init__(self, input_fileprefix, n_save_waveforms, save_channels, input_dir):
        super().__init__(input_fileprefix, n_save_waveforms, save_channels, input_dir)

    # Need to overwrite Begin(), Process(), Terminate() at least
    def Begin(self):
        # Book your analysis here
        self.BookAnalysis("ana_test1")
        self.BookAnalysis("ana_test2")

        return True

    def Process(self):

        # This will make many plots!
        # This option is time consuming
        # Comment it to analysis faster
        self.QuickPlot()
        # Do some calculation, derive some value. Use self.Fill() to store analysis result
        # Here just show how to book them into self.analysis_result
        self.Fill("ana_test1", self.scaled_voltage['CH1'][999])
        self.Fill("ana_test2", self.scaled_voltage['CH2'][999])

        return True

    def Terminate(self):

        # Print it again
        self.Print()
        # Default QuickResult and QuickHist
        self.QuickHist()
        self.QuickResult()

        return True

    # Also, you could rewrite the QuickResult and QuickHist, to modify the plot style
    # def QuickHist(self):
    #     pass

    # def QuickResult(self):
    #     pass


