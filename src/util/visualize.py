import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualize_projected_points(points: list):
    fig, ax = plt.subplots()

    for point in points:
        ax.add_patch(
            patches.Polygon(point, color='r')
        )
    plt.axis('scaled')
    plt.show()

# TODO: Implement geoplot to validate coordinate transform


if __name__ == '__main__':
    pass