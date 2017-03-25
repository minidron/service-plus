class FullPriceView extends Marionette.View
  el: '#booking-full-price'
  template: _.template "<%- toPrice(price) %>"

  templateContext: ->
    price: @price

  onChangePrice: ->
    @price = @sparePartPriceView.price + @jobPriceView.price
    @render()

  initialize: (options) ->
    @price = 0
    @sparePartPriceView = window.sparePartRootView.getChildView 'price'
    @jobPriceView = window.jobRootView.getChildView 'jobsFullPrice'
    @listenTo @sparePartPriceView, 'change:price', @onChangePrice
    @listenTo @jobPriceView, 'change:price', @onChangePrice


new FullPriceView()
