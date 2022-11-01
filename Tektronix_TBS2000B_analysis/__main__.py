import argparse
from Tektronix_TBS2000B_analysis import QuickAnalysis_Zifeng
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Standalone python data analysis skeleton wrapper")
    parser.add_argument("input_filename", type=str,
                        help="Input filename for csv files. filename prefix exactly")
    parser.add_argument("--n_save_waveforms", type=int, default=10,
                        help="N_Waveforms save in the output scripts")
    parser.add_argument("--save_channels", type=str, default="CH1,CH2",
                        help="Which channel should we save in the scripts? Example: CH1,CH2. Becarful, if you add wrong Channel here, often cause this program break down")
    parser.add_argument("--input_dir", type=str, default="./",
                        help="Where you save your data. Need full path.")
    args = parser.parse_args()
    print("This scripts is made by Zifeng Xu. Email: zifeng.xu@foxmail.com")
    print("All parameters get from parser are:")
    print(args)
    INPUT_FILENAME = args.input_filename
    N_SAVE_WAVEFORMS = args.n_save_waveforms
    SAVE_CHANNELS = args.save_channels
    INPUT_DIR = args.input_dir

    # Start Analysis
    quickanalysis = QuickAnalysis_Zifeng(
        INPUT_FILENAME, N_SAVE_WAVEFORMS, SAVE_CHANNELS, INPUT_DIR)
    quickanalysis.RunAnalysis()

    print("Goodbye!")
