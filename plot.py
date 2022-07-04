#! /usr/bin/python3

import os
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rc('font', size=12)          # controls default text sizes
plt.rc('axes', titlesize=12)     # fontsize of the axes title
plt.rc('axes', labelsize=12)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)    # legend fontsize

class bcolors:
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    BLUE = '\033[94m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def parse_data(file_path, conference_list):
    for dir in glob.glob(f'{file_path}/conferences/*'):
        dir = dir.split('/')[-1]
        conference_list.append(dir)
        os.makedirs(f"{file_path}/plots/{dir}", exist_ok=True)

        # for all conferences in a category
        for filename in glob.glob(f'{file_path}/conferences/{dir}/*'):
            file = (filename.split('/')[-1]).split('.', 1)[0]

            with open(filename) as data_file:
                data[file] = dict()
                data[file]['Conference'] = dir
                data[file]['Path'] = filename
                data[file]['Years'] = dict()
                for line in data_file:
                    info = line.split()
                    if len(info) != 3:
                        print(f"MISSING: {dir}/{file} is missing information.\
 Has to be in the format of: \n{bcolors.BLUE}<Year> <# Submissions> <# Accepted>\n{bcolors.BOLD}{bcolors.WARNING}Skipping entry {' '.join(map(str, info))} in {dir}/{file}{bcolors.ENDC}")
                    else:
                        year = info[0]
                        data[file]['Years'][year] = dict()
                        data[file]['Years'][year]['Submissions'] = info[1]
                        data[file]['Years'][year]['Accepted'] = info[2]
                        data[file]['Years'][year]['Acceptance Rate'] = int(info[2])/int(info[1])*100

def generate_plots(data, conference_list):
    markers = ["x", "o", "d", "^", ".", ",", "v", "^", "<", ">", "1", "2", "3"]
    colors = ["green", "blue", "red", "black", "brown", "gray", "olive", "cyan", "purple", "khaki", "lime", "peru", "orangered"]
    iter = 0
    for conference_group in conference_list:
        fig, ax = plt.subplots()

        handles = []
        for key, conf in data.items():
            if conf['Conference'] == conference_group:
                years = []
                acceptance_rates = []
                for year, stats in conf['Years'].items():
                    years.append(year)
                    acceptance_rates.append(stats['Acceptance Rate'])
                    
                zipped = sorted(zip(years, acceptance_rates))
                years, acceptance_rates = zip(*zipped)
                handles.append(plt.Line2D([], [], color=colors[iter], marker=markers[iter], label=key))
                ax.plot(years, acceptance_rates, markersize=6, marker=markers[iter], color=colors[iter])
                iter+=1

        fig.tight_layout()
        ax.grid(which='major', linestyle='dashed', linewidth='1')
        ax.set_axisbelow(True)
        ax.legend(loc='best', handles=handles)
        ax.set_ylim(ymin=0)
        ax.set_ylabel("Acceptance Rate (%)")
        ax.set_xlabel("Year")
        plt.savefig(f"{file_path}/plots/{conference_group}.png", bbox_inches="tight")
        plt.clf()

if __name__ == "__main__":
    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])
    data = dict()
    conference_list = []
    parse_data(file_path, conference_list)
    generate_plots(data, conference_list)
