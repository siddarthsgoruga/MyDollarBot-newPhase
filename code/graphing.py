import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

# Function to add labels to the bar chart
def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i] // 2, y[i], ha='center')

# Function to visualize and save the expenditure bar chart
def visualize(total_text, budgetData):
    # Set the color for the bars
    colors = ['red', 'cornflowerblue', 'greenyellow', 'orange', 'violet', 'grey']
    
    # Extract and summarize the expenditure by categories
    total_text_split = [line for line in total_text.split('\n') if line.strip() != '']
    categ_val = {}

    # summarize the expense by categories
    for i in total_text_split:
        a = i.split(' ')
        a[1] = a[1].replace("$", "")
        categ_val[a[0]] = float(a[1])

    # Set categories as x-axis and expenditure amount as y-axis
    x = list(categ_val.keys())
    y = list(categ_val.values())

    # Create a bar chart with expenditure data
    plt.bar(categ_val.keys(), categ_val.values(), color=colors, edgecolor='black')
    addlabels(x, y)

    plt.ylabel("Expenditure")
    plt.xlabel("Categories")
    plt.xticks(rotation=45)

    # Plot budget as horizontal lines
    lines = []
    labels = []
    if isinstance(budgetData, str):
        # If budget data is a string, it represents the overall budget
        lines.append(plt.axhline(y=float(budgetData), color="r", linestyle="-"))
        labels.append("overall budget")
    elif isinstance(budgetData, dict):
        # If budget data is a dictionary, it represents category budgets
        colorCnt = 0
        # to avoid the budget override by each others, record the budget and adjust the position of the line
        duplicate = {}
        for key in budgetData.keys():
            val = budgetData[key]
            plotVal = float(val)
            if val in duplicate:
                # if duplicate, move line upwards
                plotVal += 2 * duplicate[val]
            lines.append(plt.axhline(y=plotVal, color=colors[colorCnt % len(colors)], linestyle="-"))

            # record the amount
            duplicate[val] = duplicate[val] + 1 if val in duplicate else 1
            labels.append(key)
            colorCnt += 1

    plt.legend(lines, labels)
    plt.savefig('expenditure.png', bbox_inches='tight')

    # clean the plot to avoid the old data remains on it
    plt.clf()
    plt.cla()
    plt.close()

# Function to visualize and save the expenditure pie chart  
def vis(total_text):
    total_text_split = [line for line in total_text.split('\n') if line.strip() != '']
    categ_val = {}
    for i in total_text_split:
        a = i.split(' ')
        a[1] = a[1].replace("$", "")
        categ_val[a[0]] = float(a[1])

    x = list(categ_val.keys())
    y = list(categ_val.values())
    
    # Create a pie chart with expenditure data
    plt.clf()
    plt.pie(y, labels=x, autopct='%.1f%%')
    
    # Save the chart as "pie.png"
    plt.savefig('pie.png')

# Function to visualize and save the expenditure bar chart
def viz(total_text):
    total_text_split = [line for line in total_text.split('\n') if line.strip() != '']
    categ_val = {}
    for i in total_text_split:
        a = i.split(' ')
        a[1] = a[1].replace("$", "")
        categ_val[a[0]] = float(a[1])

    x = list(categ_val.keys())
    y = list(categ_val.values())

    # Create a bar chart with expenditure data
    plt.clf()
    plt.bar(categ_val.keys(), categ_val.values(), color=[(1.00, 0, 0, 0.6), (0.2, 0.4, 0.6, 0.6), (0, 1.00, 0, 0.6), (1.00, 1.00, 0, 1.00)], edgecolor='blue')
    addlabels(x, y)

    plt.ylabel("Expenditure")
    plt.xlabel("Categories")
    plt.xticks(rotation=45)

    # Save the chart as "expend.png"
    plt.savefig('expend.png', bbox_inches='tight')