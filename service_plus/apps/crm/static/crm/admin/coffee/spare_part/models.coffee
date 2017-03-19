class SparePartApp.BaseModel extends Backbone.Model
  url: ->
    "#{@urlRoot}/#{@id}/"

  urlRoot: ''

  sync: (method, model, options) ->
    csrfSafeMethod = (method) ->
      /^(GET|HEAD|OPTIONS|TRACE)$/.test method

    options.beforeSend = (xhr, settings) ->
      if !csrfSafeMethod(settings.type) and !@crossDomain
        csrf = $('[name=csrfmiddlewaretoken]').val()
        xhr.setRequestHeader 'X-CSRFToken', csrf
    super method, model, options


class SparePartApp.BookingSparePart extends SparePartApp.BaseModel
  defaults:
    title: ''
    retail_price: 0

  urlRoot: '/api/spare_part_count'



class SparePartApp.BookingSpareParts extends Backbone.Collection
  model: SparePartApp.BookingSparePart

  url: ->
    booking_id = parseInt(location.pathname.split( '/' ).filter((e) ->
      e).slice(-2, -1)[0])
    "/api/spare_part_count/?booking=#{booking_id}"

bookingSpareParts = new SparePartApp.BookingSpareParts()



class SparePartApp.SparePart extends SparePartApp.BaseModel
  defaults:
    id: 0
    title: ''
    retail_price: 0
    count: 0

  urlRoot: '/api/spare_part'



class SparePartApp.SpareParts extends Backbone.Collection
  model: SparePartApp.SparePart

  url: ->
    filter_el = $ '#device-model'
    brand_id = filter_el.data 'brand'
    model_id = filter_el.data 'model'
    filters = "brand=#{brand_id}&model=#{model_id}"
    "/api/spare_part/?#{filters}"

spareParts = new SparePartApp.SpareParts()
