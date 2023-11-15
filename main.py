import tkinter as tk
import math

dt = 200
def drawline(a,b,canvas):
    canvas.delete("hull")
    canvas.create_line(a[0], a[1], b[0], b[1], fill="blue", tags="hull")
    canvas.after(dt)
    canvas.update()




def euclid_dist(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2




def open_algorithm_window(algorithm):
    window = tk.Toplevel(app)
    window.title(algorithm)


    canvas = tk.Canvas(window, width=800, height=600, bg='white')
    canvas.pack()


    points = []


    def add_point(event):
        x, y = event.x, event.y
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="pink")
        canvas.create_text(x, y-10,text=f"{x},{y}", fill="black")
        points.append((x,y))


    canvas.bind("<Button-1>", lambda event: add_point(event))
   
   
    button_find_hull = tk.Button(window, text=f"Find Convex Hull for {algorithm}", command=lambda: find_convex_hull(points, canvas, algorithm), bg='lightblue', fg='black')  # Set button background and foreground (text) colors
    button_find_hull.pack()


def find_convex_hull(points, canvas, algorithm):


    points.sort()
    d,p1,p2= closest_pair(points, canvas)
    canvas.delete("hull")
    print(d,p1,p2)
    drawline(p1,p2,canvas)
    # algos[algorithm](points, canvas)
           
    # for h in hullstates:
    #     draw_hull(h, canvas, "red")


   


def draw_hull(hull, canvas):
    color = "red"
    canvas.delete("hull")
    for i in range(len(hull) - 1):
        x1, y1 = hull[i]
        x2, y2 = hull[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill=color, tags="hull")
    canvas.after(dt)
    canvas.update()


def cross(a, b, c):
    return (c[0] - a[0])*(b[1] - a[1])  - (b[0] - a[0])*(c[1] - a[1])




def closest_pair(points, canvas):
    n = len(points)
    if n <= 1:
        return 10000000,(-1,-1),(-1,-1)
   
    left = points[:int(n/2)]
    right = points[int(n/2):]


    mx = left[-1][0]
    mp = left[-1]




    d1 = closest_pair(left, canvas)
    d2 = closest_pair(right, canvas)
   

    d, p1, p2 = d1
    if d2[0] < d1[0]:
        d, p1, p2 = d2
    stripe = []

    for p in left:
        if d > (mx - p[0])**2:
            drawline(mp, p, canvas)
            stripe.append(p[:])
    for p in right:
        if d > (p[0] - mx)**2:
            drawline(mp, p, canvas)
            stripe.append(p[:])


    m = len(stripe)
    canvas.create_line(mx, 0, mx, 600, fill="red", tags="line")


    stripe.sort(key=lambda p: p[1])


    for i in range(0, m):
       for j in range(i+1, m):
            if (stripe[j][1] - stripe[i][1])**2 > d:
                break
            drawline(stripe[i], stripe[j], canvas)
            d3=euclid_dist(stripe[i], stripe[j])
            if d>d3:
                d=d3
                p1 = stripe[i]
                p2 = stripe[j]


    canvas.delete("line")
    # drawline(p1, p2, canvas)




 
    return (d,p1,p2)




def graham_scan(points, canvas):
    if len(points) < 3:
        return points


    start_point = min(points, key=lambda p: (p[1], p[0]))
    sorted_points = sorted(points, key=lambda p: (math.atan2(p[1]-start_point[1], p[0]-start_point[0]), p))
   
    hull = [sorted_points[0], sorted_points[1]]  


    # Iterate through the sorted points to find the convex hull
    for p in sorted_points[2:]:
        while len(hull) > 1 and cross(hull[-2], hull[-1], p) > 0:
            hull.pop()
            draw_hull(hull, canvas)
        hull.append(p)
        draw_hull(hull, canvas)
   
   
    if len(hull) >= 3 and hull[0] != hull[-1]:
        hull.append(hull[0])
        draw_hull(hull, canvas)


   


   


algos = {"Graham Scan" : graham_scan}
app = tk.Tk()
app.title("Geometric Algorithms")


button_graham_scan = tk.Button(app, text="Graham Scan", command=lambda: open_algorithm_window("Graham Scan"), bg='lightblue', fg='black')  # Set button background and foreground colors
button_graham_scan.pack()






app.mainloop()



