toPrice = (value) ->
  price = value.toString().replace /\B(?=(\d{3})+(?!\d))/g, ' '
  "#{price} р."



class SparePartApp extends Marionette.Application
  region: '#spare_part'

  onStart: ->
    @showView new SparePartApp.RootView()
    bookingSpareParts.fetch()
