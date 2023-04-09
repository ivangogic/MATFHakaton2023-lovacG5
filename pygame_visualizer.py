import pygame
from pygame import Color, Surface, Vector2, Rect
from pygame.font import Font
from math import pi
from random import randint as rnd

BL_H = 30
BL_W = 70
BRD = 4
FONT_SIZE = 35

def ptOnCurve(b, t):
    q = b.copy()
    for k in range(1, len(b)):
        for i in range(len(b) - k):
            q[i] = (1-t) * q[i][0] + t * q[i+1][0], (1-t) * q[i][1] + t * q[i+1][1]
    return round(q[0][0]), round(q[0][1])

def bezier(surf, b, samples, color, thickness):
    pts = [ptOnCurve(b, i/samples) for i in range(samples+1)]
    pygame.draw.lines(surf, color, False, pts, thickness)

class Arrow:
    def __init__(self, start, end) -> None:
        self.start = Vector2(start)
        self.end = Vector2(end)

    def __repr__(self) -> str:
        return f"Arrow(start={self.start},end={self.end})"
    
    def draw(self, window, color='blue'):
        diff = self.start-self.end
        diff.x = 0
        b_points = [
            self.start, 
            self.start+Vector2(30,0),
            self.start+Vector2(50,0)-diff/1.5,
            self.end+Vector2(-50,0)+diff/1.5,
            self.end+Vector2(-30,0),
            self.end
        ]
        bezier(window, b_points, 20, Color(color), 4)
        # pygame.draw.lines(window, Color('gray'), False, b_points, 2)

class Field:
    def __init__(self, address, v, dest=(0,0)) -> None:
        self.visualizer = v
        self.address = address
        self.dest = dest
        self.value = self.visualizer.memory[address]
        self.name = ''
        self.p_in = (0,0)
        self.p_out = (0,0)
        for name in self.visualizer.names:
            if self.visualizer.names[name][0] == address:
                self.name = name

    def __repr__(self) -> str:
        pointer = self.address in self.visualizer.pointers
        return f"Field(addr={self.address},ptr={pointer},p_in={self.p_in},p_out={self.p_out})"
    
    def set_pos(self, dest):
        x, y = dest
        self.dest = dest
    
    def get_rect(self):
        x, y = self.dest
        return Rect(x, y, BL_W*2-BRD, BL_H)

    def draw(self, window):
        x, y = self.dest
        font = Font(None, FONT_SIZE)
        pygame.draw.rect(window, Color('black'), Rect(x, y, BL_W*2-BRD, BL_H))
        pygame.draw.rect(window, Color('white'), Rect(x+BRD, y+BRD, BL_W-BRD*2, BL_H-BRD*2))
        pygame.draw.rect(window, Color('white'), Rect(x+BL_W, y+BRD, BL_W-BRD*2, BL_H-BRD*2))
        name_surface = font.render(f"{self.name}", True, Color('red'))
        self.p_in = (x-name_surface.get_rect().width, y+BL_H//2)
        self.p_out = (x+BL_W*2-BRD, y+BL_H//2)
        window.blit(name_surface, (x-BRD-name_surface.get_rect().width, y+BRD))
        window.blit(font.render(f"{self.address}", True, Color('red')), (x+BRD, y+BRD))
        window.blit(font.render(f"{self.value}", True, Color('red')), (x+BL_W, y+BRD))

class HeapBlock:
    def __init__(self, start, size, v, dest=(0,0)) -> None:
        self.start = start
        self.visualizer = v
        self.size = size
        self.dest = dest
        x, y = dest
        self.fields = [Field(start+i, self.visualizer, dest=(x, y+BL_H*i-BRD*i)) for i in range(size)]

    def draw(self, window):
        x, y = self.dest
        pygame.draw.rect(window, Color('red'), (x-2, y-2, BL_W*2+4-BRD, (BL_H)*len(self.fields)-BRD))
        for i, f in enumerate(self.fields):
            f.draw(window)

    def get_rect(self):
        x, y = self.dest
        return Rect(x-2, y-2, BL_W*2+4-BRD, (BL_H)*len(self.fields)-BRD)

    def set_pos(self, dest):
        x, y = dest
        self.dest = dest
        for i, f in enumerate(self.fields):
            f.set_pos( (x, y+BL_H*i-BRD*i))


class Visualizer:

    def __init__(self, state) -> None:
        self.memory, self.names, self.heap = state
        self.pointers = {}
        print(f"memory={self.memory}")
        print(f"names={self.names}")
        print(f"heap={self.heap}")

        self.pointers = {}
        for dest in self.heap.keys():
            for addr in self.memory:
                if self.memory[addr] == dest:
                    self.pointers[addr] = dest
        for name in self.names:
            if self.names[name][1]:
                self.pointers[self.names[name][0]] = self.memory[self.names[name][0]]
                # pointers.append(names[name][0])

        pygame.init()
        self.window = pygame.display.set_mode((800,800))
        pygame.display.set_caption('Memory view')

        self.heap_blocks = [HeapBlock(addr, siz, self) for addr, siz in self.heap.items()]
        used = []
        for hb in self.heap_blocks:
            hb.set_pos((rnd(10,70)*10, rnd(10,70)*10))
            for f in hb.fields:
                used.append(f.address)
        self.stack_fields = [Field(addr, self) for addr in self.memory.keys() if addr not in used]
        for f in self.stack_fields:
            f.set_pos((rnd(10,70)*10, rnd(10,70)*10))
        arrows = []
        
        print(f"pointers={self.pointers}")
        all_fields = [f for f in self.stack_fields]
        for hb in self.heap_blocks:
            for f in hb.fields:
                all_fields.append(f)
        self.all_fields = dict([(f.address, f) for f in all_fields ])

        self.colors = ['aqua', 'green', 'pink', 'yellow', 'teal', 'wheat']

        self.mainloop()

    def mainloop(self):
        dragging = False
        drag_start = None
        dragged_object = None
        dragged_object_start_pos = None
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragging = True
                    drag_start = pygame.mouse.get_pos()
                    for f in self.stack_fields[::-1]:
                        if f.get_rect().collidepoint(drag_start):
                            dragged_object = f
                            dragged_object_start_pos = f.dest
                            break
                    if not dragged_object:
                        for hb in self.heap_blocks[::-1]:
                            if hb.get_rect().collidepoint(drag_start):
                                dragged_object = hb
                                dragged_object_start_pos = hb.dest
                                break
                if event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                    dragged_object = None
        
            self.window.fill(Color('white'))

            if dragging and dragged_object:
                new_pos = Vector2(pygame.mouse.get_pos()) - drag_start + dragged_object_start_pos
                dragged_object.set_pos(new_pos)

            for i, b in enumerate(self.heap_blocks):
                b.draw(self.window)

            for i, f in enumerate(self.stack_fields):
                f.draw(self.window)
            
            # print(self.pointers)
            for ptr, dest in self.pointers.items():
                try:
                    a = Arrow(
                        start=self.all_fields[ptr].p_out,
                        end=self.all_fields[dest].p_in
                    )
                    a.draw(self.window, color=self.colors[ptr%len(self.colors)])
                except:
                    pass

            pygame.display.flip()
        
            if not running:
                pygame.display.quit()

"""

int main() {
int **mat = malloc(3);
*(mat) = malloc(3);
*(mat+1) = malloc(3);
*(mat+2) = malloc(3);
}

"""
