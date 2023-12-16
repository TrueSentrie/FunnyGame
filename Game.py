import pygame
import time

pygame.init()

ScreenWidth=800
ScreenHeight=600

Screen=pygame.display.set_mode((ScreenWidth,ScreenHeight))

TextFont=pygame.font.SysFont("Arial",30)

def DrawText(Text,Font,Color,x,y):
    img=Font.render(Text,True,Color)
    Screen.blit(img,(x,y))

def HpOverflowHandler(HealthMod):
    if Stats.Overhealth>0:
        Temp=Stats.Overhealth+HealthMod
        DamageToHP=0
        while Temp<0:
            Temp+=1
            DamageToHP+=1
        else:
            Stats.Overhealth-=HealthMod
        Stats.Hp-=DamageToHP
    else:
        NewHealth=HealthMod+Stats.Hp
        while NewHealth>Stats.MaxHp:
            NewHealth-=1
            Stats.Overhealth+=1
        Stats.Hp=NewHealth

class StartStats():
    def __init__(self,Atk,MaxHp,Hp,Def,XP,NextLvl,Luck,Overhealth,x,y,w,h):
        self.Atk=10
        self.MaxHp=100
        self.Hp=100
        self.Def=20
        self.Xp=0
        self.NextLvl=100
        self.Luck=0.05
        self.Overhealth=0
        self.x=x
        self.y=y
        self.w=w
        self.h=h

    def Draw(self,surface):
        Ratio=self.Hp/self.MaxHp
        OHRatio=self.Overhealth/self.MaxHp
        pygame.draw.rect(surface,"Red",(self.x,self.y,self.w,self.h))
        pygame.draw.rect(surface,"Green",(self.x,self.y,self.w*Ratio,self.h))
        if self.Overhealth>0:
            pygame.draw.rect(surface,"Blue",(self.x,self.y,self.w*OHRatio,self.h))

class Inventory():
    def __init__(self,MedKits,Money):
        self.MedKits=2
        self.Money=0
        
Inv=Inventory(MedKits=2,Money=0)
Stats=StartStats(Atk=10,MaxHp=100,Hp=100,Def=20,XP=0,NextLvl=100,Luck=0.05,Overhealth=0,x=250,y=540,w=300,h=40)

MoneyReqOne=False

Run=True
Seconds=0
LastInc=time.time()
DamageOverTime=1
dotThreshold=10

while Run:
    Screen.fill((0,0,0))

    Stats.Draw(Screen)
    if time.time()>=LastInc+1:
        if Seconds>=dotThreshold:
            DamageOverTime+=1
            dotThreshold+=10
            print(f"DOT:{DamageOverTime}")
            print(f"DOT Threshold:{dotThreshold}")

        Seconds+=1
        if Stats.Overhealth>0:
            HpOverflowHandler(DamageOverTime)
        else:
            Stats.Hp-=DamageOverTime
        LastInc=time.time()

    DrawText(f"Time:{Seconds}s",TextFont,(255,255,255),600,0)
    DrawText(f"Damage Over Time:{DamageOverTime}",TextFont,(255,255,255),480,40)
    DrawText(f"Money: {Inv.Money}",TextFont,(255,255,255),0,0)
    DrawText(f"MedKits: {Inv.MedKits}",TextFont,(255,255,255),250,500)
    DrawText("Stats",TextFont,(255,255,255),0,80)

    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_g:
                Seconds+=10
                DamageOverTime+=1
                dotThreshold+=10
            if event.key==pygame.K_e:
                HpOverflowHandler(-10)
            if event.key==pygame.K_q:
                Inv.MedKits+=1
            if event.key==pygame.K_SPACE:
                HpOverflowHandler(10)
            if event.key==pygame.K_h and Inv.MedKits>0:
                HpOverflowHandler(Stats.MaxHp/2)
                Inv.MedKits-=1
        if event.type==pygame.MOUSEBUTTONDOWN:
            Inv.Money+=1
        if event.type==pygame.QUIT:
            Run=False
    if Inv.Money>=20 or MoneyReqOne:
        MoneyReqOne=True
        DrawText("Open Shop",TextFont,(255,255,255),0,40)


    pygame.display.flip()
    pygame.display.update()

pygame.quit()