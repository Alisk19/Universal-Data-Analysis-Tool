import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

class DataAnalyzer:
    def __init__(self, data):
        self.data = data
        self.numeric_columns = self.data.select_dtypes(include='number').columns.tolist()

    def clean_data(self, selected_columns=None):
        df = self.data.drop_duplicates()
        if selected_columns is None:
            selected_columns = self.numeric_columns
        for col in selected_columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df = df.dropna(subset=selected_columns)
        return df

    def calculate_pass_fail(self, threshold, selected_columns=None):
        df = self.data.copy()
        if selected_columns is None:
            selected_columns = self.numeric_columns
        df["Pass"] = (df[selected_columns] >= threshold).all(axis=1).map({True: "Pass", False: "Fail"})
        return df

    def pass_fail_summary(self):
        if "Pass" in self.data.columns:
            return self.data["Pass"].value_counts().reset_index().rename(
                columns={"index": "Status", "Pass": "Count"}
            )
        else:
            return pd.DataFrame({"Status": [], "Count": []})

    def subject_statistics(self, selected_columns=None):
        if selected_columns is None:
            selected_columns = self.numeric_columns
        return self.data[selected_columns].describe().loc[["mean", "min", "max"]]

    def top_performers(self, n=5, selected_columns=None, name_column=None):
        if selected_columns is None:
            selected_columns = self.numeric_columns
        if "Percentage" not in self.data.columns:
            self.data["Percentage"] = self.data[selected_columns].mean(axis=1)
        cols = [name_column] if name_column and name_column in self.data.columns else []
        return self.data.nlargest(n, "Percentage")[cols + ["Percentage"] + selected_columns]

    def grade_distribution(self, selected_columns=None):
        if selected_columns is None:
            selected_columns = self.numeric_columns
        if "Percentage" not in self.data.columns:
            self.data["Percentage"] = self.data[selected_columns].mean(axis=1)
        bins = [0, 40, 60, 80, 90, 100]
        labels = ["F", "D", "C", "B", "A"]
        self.data["Grade"] = pd.cut(self.data["Percentage"], bins=bins, labels=labels, right=False)
        return self.data["Grade"].value_counts().sort_index()

    def get_subject_grades(self, subject):
        bins = [0, 40, 60, 80, 90, 100]
        labels = ["F", "D", "C", "B", "A"]
        grades = pd.cut(self.data[subject], bins=bins, labels=labels, right=False)
        return grades.value_counts().sort_index()

    def plot_grade_comparison(self, subject1, subject2):
        grades_sub1 = self.get_subject_grades(subject1)
        grades_sub2 = self.get_subject_grades(subject2)
        df = pd.DataFrame({subject1: grades_sub1, subject2: grades_sub2})
        fig, ax = plt.subplots(figsize=(10, 6))
        df.plot(kind="bar", ax=ax, color=["#1f77b4", "#ff7f0e"])
        ax.set_title(f"Grade Comparison: {subject1} vs {subject2}", fontsize=14)
        ax.set_xlabel("Grade", fontsize=12)
        ax.set_ylabel("Number of Students", fontsize=12)
        ax.legend(title="Subjects")
        plt.xticks(rotation=0)
        return fig

    def weak_students(self, threshold, selected_columns=None, name_column=None):
        if selected_columns is None:
            selected_columns = self.numeric_columns
        weak_students = self.data[self.data[selected_columns].lt(threshold).any(axis=1)]
        cols = [name_column] if name_column and name_column in self.data.columns else []
        return weak_students[cols + selected_columns]

    def subject_pass_fail_rates(self, selected_columns=None):
        if selected_columns is None:
            selected_columns = self.numeric_columns
        pass_rates = {}
        for col in selected_columns:
            pass_rates[col] = (self.data[col] >= 40).mean() * 100
        return pd.Series(pass_rates)

    def trend_analysis(self, time_column, selected_columns=None):
        if selected_columns is None:
            selected_columns = self.numeric_columns
        if time_column in self.data.columns:
            return self.data.groupby(time_column)[selected_columns].mean()
        else:
            return pd.DataFrame({"Error": ["Time column not found."]})

    def plot_pass_fail_pie(self):
        if "Pass" not in self.data.columns:
            st.warning("No 'Pass' column to plot.")
            return
        fig, ax = plt.subplots()
        self.data["Pass"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
        ax.set_ylabel("")
        return fig

    def plot_subject_histograms(self, selected_columns=None):
        if selected_columns is None:
            selected_columns = self.numeric_columns
        fig, ax = plt.subplots()
        self.data[selected_columns].plot.hist(alpha=0.5, ax=ax)
        return fig

    def plot_correlation_heatmap(self, selected_columns=None):
        if selected_columns is None:
            selected_columns = self.numeric_columns
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(
            self.data[selected_columns].corr(),
            annot=True, cmap="coolwarm", vmin=-1, vmax=1, cbar=True, ax=ax
        )
        ax.set_title("Correlation Heatmap", fontsize=14)
        ax.set_xlabel("Columns", fontsize=12)
        ax.set_ylabel("Columns", fontsize=12)
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        return fig

    def plot_grade_distribution(self, selected_columns=None):
        fig, ax = plt.subplots()
        self.grade_distribution(selected_columns).plot(kind="bar", color="skyblue", ax=ax)
        ax.set_title("Overall Grade Distribution")
        ax.set_xlabel("Grade")
        ax.set_ylabel("Number of Students")
        return fig

    def plot_pass_fail_ratio(self):
        if "Pass" not in self.data.columns:
            st.warning("No 'Pass' column to plot.")
            return
        fig, ax = plt.subplots()
        pass_fail_counts = self.data["Pass"].value_counts()
        pass_fail_counts.plot.pie(
            autopct="%1.1f%%", colors=["lightgreen", "lightcoral"],
            labels=pass_fail_counts.index, ax=ax
        )
        ax.set_title("Pass/Fail Ratio")
        ax.set_ylabel("")
        return fig

    def get_student_by_roll(self, roll_number, roll_column="Roll Number"):
        if roll_column in self.data.columns:
            student = self.data[self.data[roll_column] == roll_number]
            return student.iloc[0] if not student.empty else None
        return None

    def plot_student_comparison(self, student1, student2, selected_columns, roll1=None, roll2=None):
        if not selected_columns:
            raise ValueError("Select at least one column for comparison.")
        student1_scores = student1[selected_columns].tolist()
        student2_scores = student2[selected_columns].tolist()
        labels = selected_columns
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(selected_columns))
        bar_width = 0.35
        bars1 = ax.bar(x, student1_scores, bar_width, label=f"{roll1 if roll1 else 'Student 1'}", color="#1f77b4")
        bars2 = ax.bar([p + bar_width for p in x], student2_scores, bar_width, label=f"{roll2 if roll2 else 'Student 2'}", color="#ff7f0e")
        ax.set_title(f"Student Comparison", fontsize=14)
        ax.set_xlabel("Columns", fontsize=12)
        ax.set_ylabel("Scores", fontsize=12)
        ax.set_xticks([p + bar_width/2 for p in x])
        ax.set_xticklabels(labels, rotation=45)
        ax.legend()
        for bar in bars1 + bars2:
            height = bar.get_height()
            ax.annotate(f"{height:.1f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
        return fig

    def get_statistics(self, selected_columns=None):
        if selected_columns is None:
            selected_columns = self.numeric_columns
        return self.data[selected_columns].describe().loc[["mean", "50%", "min", "max", "std"]].rename(index={"50%": "median"})

    def compare_rows(self, row_indices, selected_columns=None):
        if selected_columns is None:
            selected_columns = self.numeric_columns
        return self.data.loc[row_indices, selected_columns]

    def plot_bar(self, row_indices, selected_columns=None):
        df = self.compare_rows(row_indices, selected_columns)
        fig, ax = plt.subplots(figsize=(10, 6))
        df.T.plot(kind="bar", ax=ax)
        ax.set_title("Bar Chart Comparison")
        ax.set_xlabel("Columns")
        ax.set_ylabel("Values")
        plt.xticks(rotation=45)
        return fig

    def plot_line(self, row_indices, selected_columns=None):
        df = self.compare_rows(row_indices, selected_columns)
        fig, ax = plt.subplots(figsize=(10, 6))
        df.T.plot(kind="line", marker='o', ax=ax)
        ax.set_title("Line Chart Comparison")
        ax.set_xlabel("Columns")
        ax.set_ylabel("Values")
        plt.xticks(rotation=45)
        return fig

    def plot_box(self, selected_columns=None):
        if selected_columns is None:
            selected_columns = self.numeric_columns
        fig, ax = plt.subplots(figsize=(10, 6))
        self.data[selected_columns].plot.box(ax=ax)
        ax.set_title("Box Plot (Distribution)")
        ax.set_xlabel("Columns")
        ax.set_ylabel("Values")
        plt.xticks(rotation=45)
        return fig

    def plot_pie(self, column):
        fig, ax = plt.subplots(figsize=(8, 8))
        data = self.data[column].value_counts()
        data.plot.pie(autopct='%1.1f%%', ax=ax, startangle=90, counterclock=False)
        ax.set_ylabel("")
        ax.set_title(f"Pie Chart of {column}")
        return fig