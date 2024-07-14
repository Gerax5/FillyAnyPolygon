import struct
def char(c):
    # 1
    return struct.pack("=c", c.encode("ascii"))

def word(w):
    #2
    return struct.pack("=h", w)

def dword(d):
    #4
    return struct.pack("=l",d)

class Render(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        
        self.glColor(1,1,1)
        self.glClearColor(0,0,0)
        self.glClear()

    def glColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.currColor = [ r, g, b]

    def glClearColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.clearColor = [r,g,b]

    def glClear(self):
        color = [int(i * 255) for i in self.clearColor]
        self.screen.fill(color)

        self.frameBuffer = [[self.clearColor for y in range(self.height)] for x in range(self.width)]

    def glPoint(self, x, y, color = None):
        # Pygame empieza a renderizar desde la esquina 
        # superior izquierda. Hay que volter el valor y

        if (0<=x<self.width) and (0 <= y <self.height):
            # Pygame recibe los colores en un rango de 0 a 255
            color = [int(i * 255) for i in (color or self.currColor)]
            self.screen.set_at((x, self.height - 1 - y), color)
            self.frameBuffer[x][y] = color

    def glLine(self, vo,  v1, color = None):
        # y = mx + b
        xo = int(vo[0])
        x1 = int(v1[0])
        yo = int(vo[1])
        y1 = int(v1[1])

        # Algoritmo de Lineas de Bresenham

        #Si el punto 0 es igual punto 1, solo se dibuja un punto
        if x1 == 1 and yo == y1:
            self.glPoint(xo,yo)
            return
        
        dy = abs(y1 - yo)
        dx = abs(x1 - xo) 

        steep = dy > dx

        if steep:
            xo, yo = yo, xo
            x1, y1 = y1, x1
        
        if xo > x1:
            xo, x1 = x1, xo
            yo, y1 = y1, yo

        dy = abs(y1 - yo)
        dx = abs(x1 - xo) 

        offset = 0
        limit = 0.75
        m = dy / dx
        y = yo

        for x in range(xo, x1 + 1):

            if steep:
                self.glPoint(y, x, color or self.currColor)
            else:
                self.glPoint(x, y, color or self.currColor)

            offset += m

            if offset >= limit:
                if yo < y1:
                    y += 1
                else:
                    y -= 1
                limit += 1

    def glGenerateFrameBuffer(self, filename):
	
        with open(filename, "wb") as file:
            # Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))
            
            # Info Header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            
            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    color = self.frameBuffer[x][y]
                    color = bytes([color[2],
                                color[1],
                                color[0]])
                    
                    file.write(color)

    def centerPolygon(self, coords):
        #Suponiendo que es cerrado
        #Formula: (1/6A) (xi + xi+1)(xiyi+1 - xi+1yi)
        coords.append(coords[0])
        a = 0
        cx = 0
        cy = 0

        for i in range(len(coords) - 1):
            x0, y0 = coords[i]
            x1, y1 = coords[i + 1]
            
            temp = x0 * y1 - x1 * y0
            
            a += temp
            cx += (x0 + x1) * temp
            cy += (y0 + y1) * temp

        a *= 0.5
        cx //= (6 * a)
        cy //= (6 * a)

        return int(cx), int(cy)

    def boundaryfill(self, x, y, fillColor = None, boundaryColor = None):
        stack = [(x, y)]
        while stack:
            x, y = stack.pop()
            if (0 <= x < self.width) and (0 <= y < self.height):
                color = [int(i * 255) for i in (boundaryColor or self.currColor)]
                if self.frameBuffer[x][y] == color:
                    continue
                self.glPoint(x, y, fillColor)
                stack.append((x + 1, y))
                stack.append((x - 1, y))
                stack.append((x, y + 1))
                stack.append((x, y - 1))

        #Alcanzo los limites de recursividad jajaja
        #self.boundaryfill(x + 1, y, fillColor, boundaryColor)
        #self.boundaryfill(x - 1, y, fillColor, boundaryColor)
        #self.boundaryfill(x, y + 1, fillColor, boundaryColor)
        #self.boundaryfill(x, y - 1, fillColor, boundaryColor)
        
        