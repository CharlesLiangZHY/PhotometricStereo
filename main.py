import sys
import read
import reconstruct
import visualize


if __name__ == "__main__":
    path = None
    index = None
    plot = 1
    num = 2
    smooth = False
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-i':
            index = sys.argv[i+1]
            if int(index) > 39:
                print("Index Error")
                break
            else:
                path = "CroppedYale/yaleB" + index
        if sys.argv[i] == '-p':
            path = sys.argv[i+1]
        if sys.argv[i] == '-t':
            if sys.argv[i+1] == "surface" or sys.argv[i+1] == "sf":
                plot = 2
            elif sys.argv[i+1] == "face" or sys.argv[i+1] == "f":
                plot = 1
            elif sys.argv[i+1] == "albedo" or sys.argv[i+1] == "a":
                plot = 3
            elif sys.argv[i+1] == "normal" or sys.argv[i+1] == "n":
                plot = 4
            elif sys.argv[i+1] == "raw" or sys.argv[i+1] == "r" or sys.argv[i+1] == "dataset" or sys.argv[i+1] == "ds" or sys.argv[i+1] == "d":
                plot = 5
        if sys.argv[i] == '-n':
            num = int(sys.argv[i+1])
        if sys.argv[i] == '-s':
            smooth = True

    if path != None:
        images, source = read.load_dataset(path)
        normals, albedo = reconstruct.reconstruct_normals(images, source)
        if plot == 3:
            visualize.plot_albedo(albedo)
        elif plot == 4:
            visualize.plot_normal(normals)
        elif plot == 5:
            visualize.plot_data(images)
        else:
            height = reconstruct.reconstruct_surface(normals, num, smooth)
            if plot == 2:
                visualize.plot_surface(height)
            if plot == 1:
                visualize.plot_face(height,albedo)
         

