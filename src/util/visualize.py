import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualize_projected_points(points, polygon_point_counts, limit):
    fig, ax = plt.subplots()

    start = 0
    for i, count in enumerate(polygon_point_counts):
        if i > limit:
            break

        end = start+count
        ax.add_patch(
            patches.Polygon(points[start:end,:], color='r')
        )
        start = end

    plt.axis('scaled')
    plt.show()

def visualize_latlon_points(filename, points, polygon_point_counts, limit):
    import folium
    import webbrowser

    m = folium.Map(location=[points[0][0], points[0][1]], zoom_start=10)

    start = 0
    for i, count in enumerate(polygon_point_counts):
        if i > limit:
            break

        end = start + count
        folium.Polygon(locations=points[start:end, :].tolist()).add_to(m)
        start = end

    html_path = f'{filename}.html'
    m.save(html_path)
    webbrowser.open(html_path, new=2)


if __name__ == '__main__':
    pass