"""
|index|Average_Rate|Count|
| 0 | 0.300400 | 4500 |
| 1 | 0.245923 | 13000 |

"""

fig, ax = plt.subplots(1,1, figsize = (12, 8))

a.plot.scatter(x = "index", y = "average_rate", s = [100, 100], marker = "D", ax = ax);
ax.annotate("Average Rate: "+"{:,.0%}".format(0.300400), xy = (-0.14, 0.300400 + 0.002), color = "k", fontsize = 12); 
ax.annotate("Average Rate: "+"{:,.0%}".format(0.245923), xy = (0.83, 0.245923 + 0.002), color = "k", fontsize = 12); 
ax.grid(b = True, which = "major", axis = "y", color = "darkgray", linestyle = '-', linewidth = 2, alpha = 0.35);
ax.patch.set_facecolor('white');
#for k in np.array(range(0,35,5))/100.0:
#    ax.axhline(y = k, color = "darkgray", linewidth = 0.5, linestyle = "-");

plt.sca(ax);
plt.title("Average Rate by Months", fontsize = 14, fontweight = "bold");
plt.xlabel("Months", fontsize = 12);
plt.ylim(0, 0.35);
plt.ylabel("Average Rate", fontsize = 12);
plt.yticks(fontsize = 12);


ax_twin = ax.twinx()
a.plot(x = "index", y = "count", kind = "bar", color = "orange", alpha = 0.20, legend = False, ax = ax_twin);
ax_twin.annotate("Group Size: "+"{:,.0f}".format(4504), xy = (-0.14, 4504 + 200), color = "k", fontsize = 12); 
ax_twin.annotate("Group Size: "+"{:,.0f}".format(12939), xy = (0.83, 12939 + 200), color = "k", fontsize = 12); 
ax_twin.grid(b = False);

plt.sca(ax_twin);
#plt.xlabel("Months", fontsize = 12);
plt.xticks([0, 1], ["[3, 12)", "[12, 50)"], fontsize = 12);
plt.ylim(0, 14000);
plt.ylabel("Group Size", fontsize = 12, rotation = 270, labelpad = 15);
plt.yticks(fontsize = 12);
