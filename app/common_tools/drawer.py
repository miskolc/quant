import matplotlib.pyplot as plt


# 画出训练后的结果
def make_training_plt(show_plot, df_x_test, df_y_test, df_y_test_pred):
    if show_plot:
        plt.scatter(df_x_test.index, df_y_test, color='black')
        plt.scatter(df_x_test.index, df_y_test_pred, color='blue')
        plt.show()
