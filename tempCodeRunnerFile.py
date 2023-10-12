@app.route('/dashboard')
def dashboard():
    enrolled_candidates = len(cv_data)
    selected_candidates = 10  # Replace with the actual number of selected candidates
    not_selected_candidates = enrolled_candidates - selected_candidates

    enrollment_selection_data = [
        go.Bar(
            x=['Enrolled', 'Selected', 'Not Selected'],
            y=[enrolled_candidates, selected_candidates, not_selected_candidates],
            marker=dict(color=['blue', 'green', 'red'])
        )
    ]

    enrollment_selection_layout = go.Layout(
        title='Enrollment and Selection Status',
        xaxis=dict(title='Status'),
        yaxis=dict(title='Number of Candidates')
    )

    enrollment_selection_fig = go.Figure(data=enrollment_selection_data, layout=enrollment_selection_layout)
    enrollment_selection_graph = enrollment_selection_fig.to_html(full_html=False)

    return render_template('dashboard.html', cv_data=cv_data, enrollment_selection_graph=enrollment_selection_graph)