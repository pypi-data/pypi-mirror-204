from .Utils import *
from .Logger import *
from .DataFetch import *
from .Portfolio import *
import pandas as pd
import numpy as np
import json
import os
import imgui

class PortfolioManager:

    def __init__(self, portfolio: Portfolio):
        self._portfolio = portfolio
        self._showWindow = True
        self._startDate = "2020-01-01"
        self._endDate = "2022-12-31"
        self._stockHistoryTextures = []
        self._stockHistoryComparisonTexture = None
        self._stocksBasedDistributionPlotTexture = None
        self._countryBasedDistributionPlotTexture = None
        self._sectorBasedDistributionPlotTexture = None
    
    def Show(self):
        """Show the portfolio in a imgui window"""
        if not self._showWindow:
            return
        
        windowExpanded, self._showWindow = imgui.begin(f"Portfolio {self._portfolio._name}", True)

        with imgui.begin_tab_bar("MainPortfolioTabBar") as tab_bar:
            if tab_bar.opened:
                with imgui.begin_tab_item("General") as item1:
                    if item1.selected:
                        self.ShowGeneralTab()

                with imgui.begin_tab_item("Analysis") as item2:
                    if item2.selected:
                        if not self._portfolio._hasAnalysis:
                            imgui.text("No analysis has been done yet")
                        else:
                            self.ShowAnalysisTab()

                with imgui.begin_tab_item("Optimizations") as item3:
                    if item3.selected:
                        imgui.text("Hello Saylor!")


        imgui.end()
    
    def ShowGeneralTab(self):
        expanded, visible = imgui.collapsing_header("Portfolio Summary")
        if expanded:
            imgui.text(f"Name: {self._portfolio._name}")
            imgui.text(f"Stocks: ")
            for i in range(len(self._portfolio._stocks)):
                imgui.text(f"    {self._portfolio._stocks[i]}: {self._portfolio._weights[i]}")
            imgui.separator()
        
        expanded, visible = imgui.collapsing_header("Portfolio Analysis")
        if expanded:
            changed, self._startDate = imgui.input_text("Start Date", self._startDate, 10)
            changed, self._endDate = imgui.input_text("End Date", self._endDate, 10)
            if imgui.button("Analyse"):
                self._portfolio.Analyse(self._startDate, self._endDate)
                self.LoadAnalysis()
        
    def ShowAnalysisTab(self):
        expanded, visible = imgui.collapsing_header("Stocks History")
        if expanded:
            imgui.push_id("StocksHistoryTab")
            for i in range(len(self._portfolio._stocks)):
                imgui.text(f"{self._portfolio._stocks[i]}")
                imgui.image(self._stockHistoryTextures[i].id, self._stockHistoryTextures[i].width, self._stockHistoryTextures[i].height)
                if imgui.button(f"Save {self._portfolio._stocks[i]} as File"):
                    SaveImageAsFile(self._stockHistoryTextures[i], ShowFileSaveWindow() + ".png")
                imgui.separator()
            
            imgui.text("Comparison")
            imgui.image(self._stockHistoryComparisonTexture.id, self._stockHistoryComparisonTexture.width, self._stockHistoryComparisonTexture.height)
            if imgui.button("Save Comparison as File"):
                SaveImageAsFile(self._stockHistoryComparisonTexture, ShowFileSaveWindow() + ".png")
            imgui.separator()
            imgui.pop_id()
        
        expanded, visible = imgui.collapsing_header("Portfolio Diversification")
        if expanded:
            imgui.text("Stocks Based Distribution")
            imgui.image(self._stocksBasedDistributionPlotTexture.id, self._stocksBasedDistributionPlotTexture.width, self._stocksBasedDistributionPlotTexture.height)
            if imgui.button("Save Stocks Based Distribution as File"):
                SaveImageAsFile(self._stocksBasedDistributionPlotTexture, ShowFileSaveWindow() + ".png")
            
            imgui.text("Country Based Distribution")
            imgui.image(self._countryBasedDistributionPlotTexture.id, self._countryBasedDistributionPlotTexture.width, self._countryBasedDistributionPlotTexture.height)
            if imgui.button("Save Country Based Distribution as File"):
                SaveImageAsFile(self._countryBasedDistributionPlotTexture, ShowFileSaveWindow() + ".png")
            
            imgui.text("Sector Based Distribution")
            imgui.image(self._sectorBasedDistributionPlotTexture.id, self._sectorBasedDistributionPlotTexture.width, self._sectorBasedDistributionPlotTexture.height)
            if imgui.button("Save Sector Based Distribution as File"):
                SaveImageAsFile(self._sectorBasedDistributionPlotTexture, ShowFileSaveWindow() + ".png")

    def UnloadAnalysis(self):
        for texture in self._stockHistoryTextures:
            DeleteGLTexture(texture.id)

        if self._stockHistoryComparisonTexture != None:
            DeleteGLTexture(self._stockHistoryComparisonTexture.id)
    
        if self._stocksBasedDistributionPlotTexture != None:
            DeleteGLTexture(self._stocksBasedDistributionPlotTexture.id)

        if self._countryBasedDistributionPlotTexture != None:
            DeleteGLTexture(self._countryBasedDistributionPlotTexture.id)
        
        if self._sectorBasedDistributionPlotTexture != None:
            DeleteGLTexture(self._sectorBasedDistributionPlotTexture.id)

    def LoadAnalysis(self):
        self.UnloadAnalysis()
        self._stockHistoryTextures = [ CreateGLTexture(self._portfolio._analysis.stockHistoryPlots[i]) for i in range(len(self._portfolio._stocks)) ]
        self._stockHistoryComparisonTexture = CreateGLTexture(self._portfolio._analysis.stockHistoryComparisonPlot)
        self._stocksBasedDistributionPlotTexture = CreateGLTexture(self._portfolio._analysis.stocksBasedDistributionPlot)
        self._countryBasedDistributionPlotTexture = CreateGLTexture(self._portfolio._analysis.countryBasedDistributionPlot)
        self._sectorBasedDistributionPlotTexture = CreateGLTexture(self._portfolio._analysis.sectorBasedDistributionPlot)