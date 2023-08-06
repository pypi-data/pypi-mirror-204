import imgui
from .Utils import *
from .Portfolio import *
from .PortfolioManager import *
from .Tickers import *

class PortfolioInputWindow :
    def __init__(self):
        self._title = "Portfolio Input"
        self._portfolioStocks = []
        self._portfolioName = "Portfolio 0"
        self._portfolios = []
        self._startDate = "2020-01-01"
        self._endDate = "2022-12-31"
    
    def ShowExistingPortfoliosPopup(self):
        """Show a popup modal with a list of existing portfolios to choose from and a button to remove them or open them"""
        with imgui.begin_popup_modal("Existing Portfolios") as select_popup:
            if select_popup.opened:
                for portfolio in self._portfolios:
                    imgui.text(portfolio._portfolio._name)
                    imgui.same_line()
                    if imgui.button("Open"):
                        portfolio._showWindow = True
                        imgui.close_current_popup()
                    imgui.same_line()
                    if imgui.button("Remove"):
                        self._portfolios.remove(portfolio)
                imgui.separator()
                if imgui.button("Close"):
                    imgui.close_current_popup()
            
    def Show(self):
        imgui.begin(self._title)

        if imgui.button("Add Stock"):
            stockItem = Object()
            stockItem.tickerId = 0
            stockItem.quantity = 10
            self._portfolioStocks.append(stockItem)
        
        imgui.same_line()

        if imgui.button("Clear All"):
            self._portfolioStocks.clear()
        
        if imgui.button("Add Portfolio") and len(self._portfolioStocks) > 0:
            totalStocksInPortfolio = sum([stock.quantity for stock in self._portfolioStocks])
            weights = [stock.quantity / totalStocksInPortfolio for stock in self._portfolioStocks]
            stocks = [list(STOCK_TICKER_NAMES.keys())[stock.tickerId] for stock in self._portfolioStocks]
            portfolio = Portfolio(self._portfolioName, stocks, weights, None)
            self._portfolios.append(PortfolioManager(portfolio))
            self._portfolioStocks.clear()
            self._portfolioName = f"Portfolio {len(self._portfolios)}"
        
        imgui.same_line()

        if imgui.button("Select Existing Portfolio"):
            imgui.open_popup("Existing Portfolios")

        self.ShowExistingPortfoliosPopup()

        changed, self._portfolioName = imgui.input_text("Portfolio Name", self._portfolioName)

        for stock in self._portfolioStocks:
            imgui.separator()
            imgui.push_id(str(stock))
            stock.tickerId = ImGuiShowComboBox("Ticker", list(STOCK_TICKER_NAMES.values()), stock.tickerId)
            changed, stock.quantity = imgui.slider_int("Quantity", stock.quantity, 0, 100)
            if imgui.button("Remove"):
                self._portfolioStocks.remove(stock)
                imgui.pop_id()
                break
            imgui.pop_id()

        imgui.separator()       
        imgui.end()

        for portfolio in self._portfolios:
            portfolio.Show()