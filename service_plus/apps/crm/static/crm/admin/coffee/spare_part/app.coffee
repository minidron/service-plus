toPrice = (value) ->
  price = value.toString().replace /\B(?=(\d{3})+(?!\d))/g, ' '
  "#{price} р."



class SparePartApp extends Marionette.Application
  region: '#spare_part'

  onStart: ->
    window.sparePartRootView = new SparePartApp.RootView()
    @showView window.sparePartRootView
    bookingSpareParts.fetch()
