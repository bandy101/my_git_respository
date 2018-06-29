##Chess names：
##    Red Black
##0 = blank
##1 = 帥  將  king
##2 = 仕  士  guard
##3 = 相	象   elephant
##4 = 傌	馬   horse
##5 = 俥	車   tank
##6 = 炮	砲   cannon
##7 = 兵	卒   soldier


from Model import *
import ccGUI


def initialBoard():
    '''
        initial the game board
    '''
    point_list = []    
    counter = 0
    initial_string = CC_BOARD_SEQUENCE
    for rows in range(10):
        row_list = []
        fy = D_VERTICAL*rows+PADDING_Y
        for columns in range(9):
            fx = D_HORIZONTAL*columns+PADDING_X
            chess = _convertNumToChessCode(fx,fy,initial_string[counter],'Black')  
            if counter >= 10*9/2:
                chess = _convertNumToChessCode(fx,fy,initial_string[counter],'Red')
            row_list.append(chess)
            counter+=1
        fx += 1
        point_list.append(row_list)
    
    return point_list


def _convertNumToChessCode(fx,fy,type_num,color = None)->object:
    '''
        initialBoard helper function
    '''
    type_list = [BasePoint(fx,fy,None),                        #0None   
                 BasePoint(fx,fy,King(type_num,color)),        #1King   
                 BasePoint(fx,fy,Guard(type_num,color)),       #2Guard  
                 BasePoint(fx,fy,Elephant(type_num,color)),    #3Elephant   
                 BasePoint(fx,fy,Horse(type_num,color)),       #4Horse  
                 BasePoint(fx,fy,Tank(type_num,color)),        #5Tank   
                 BasePoint(fx,fy,Cannon(type_num,color)),      #6Cannon
                 BasePoint(fx,fy,Soldier(type_num,color))]     #7Soldier
    return type_list[int(type_num)]


def touchChess(func):
    def wrapper(*args):
        event,game,player,width,height,special_chess = args
        for rows in game:
            for base_point in rows:
                if (base_point.contain(_getPointFraction(event,width,height))
                    and base_point.content[0] != None):
                    special_chess = base_point.content[0]
                    return func(event,game,player,width,height,special_chess)
    return wrapper

@touchChess
def grabChess(event,game,player,width,height,chess):
    if chess.returnColorType() == player:
        chess.grabbedChess()
        return True
    return False

@touchChess
def giveUpGrab(event,game,player,width,height,chess):
    if chess.returnBgColor() == 'Grey':
        chess.grabbedChess()
        return True
    return False
            

 
           



def _getPointPixel(event):
    '''
    print out the clicked point information
    '''
    return event.x,event.y


def _getPointFraction(event,*args):
    return event.x/args[0],event.y/args[1]


def printConsoleBoard(gameState: iter):
    '''
        print out the board on console
    '''
    for row in gameState:
        for col in row:
            if col.content[0] == None:
                print('.', end = " ")
            else:
                print(col.content[0].returnNumType(), end = " ")
        print()
        

def validMove(gameState:list):
    pass



        






