# -*- coding: utf-8 -*-
import os,pygame

class TopicMenu:
    def __init__(self,game):
        self.Game = game
        self.visible = False
        self.rect = pygame.Rect(0,668,1024,100)
        self.topics = []
        self.currentTopic = None
        
    def loadCharacterTopics(self,character):
        self.clearTopics()
        self.topics = character.topics
        self.arrangeTopics()
        
    def arrangeTopics(self):
        currentY = 720
        currentX = 25
        for topic in self.topics:
            if currentX + topic.render.get_width() < 1024:
                topic.setPos((currentX,currentY))
                currentX += topic.render.get_width()+25
            else:
                currentY -= 35
                currentX = 25
                topic.setPos((currentX,currentY))
                currentX += topic.render.get_width()+25

    def setCurrentTopic(self,topic):
        self.currentTopic = topic
        topic.setActive()
    
    def clearCurrentTopic(self):
        self.currentTopic = None
        for topic in self.topics:
            topic.clearActive()
            
    def getCurrentTopic(self):
        return self.currentTopic
        
    def clearTopics(self):
        self.topics = []
                        
    def show(self):
        self.visible = True
        
    def hide(self):
        self.visible = False
        self.clearTopics()
