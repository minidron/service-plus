class SparePartApp.RootView extends Marionette.View
  ###
  Главная вью
  ###
  template: _.template """
  <table id="spare_part-form">
    <thead>
      <tr>
        <th>Запчасть</th>
        <th>Гарантия</th>
        <th>Цена</th>
        <th></th>
      </tr>
    </thead>

    <tbody id="spare_part-list"></tbody>

    <tfoot>
      <tr id="spare_part-add" colspan="2"></tr>
      <tr id="spare_part-price"></tr>
    </tfoot>
  </table>

  <div id="spare_part-popup" class="closed">
    <div id="available-spare_part">
      <table>
        <thead>
          <tr>
            <th>Запчасть</th>
            <th>Гарантия</th>
            <th>Кол-во</th>
            <th>Цена</th>
          </tr>
        </thead>
        <tbody id="available-spare_part-list"></tbody>
      </table>
    </div>
    <div class="overlay"></div>
  </div>
  """

  regions:
    sparePartForm:
      el: '#spare_part-list'
      replaceElement: true
    sparePartAdd:
      el: '#spare_part-add'
      replaceElement: true
    popup:
      el: '#available-spare_part-list'
      replaceElement: true
    price:
      el: '#spare_part-price'
      replaceElement: true

  ui:
    popup: '#spare_part-popup'
    overlay: '#spare_part-popup .overlay'

  events:
    'click @ui.popup': 'closePopup'

  closePopup: (event) ->
    if event.target is @ui.overlay[0]
      @trigger 'close:popup'

  onOpenPopup: (view, event) ->
    @ui.popup.removeClass 'closed'
    popupView = @getChildView 'popup'
    popupView.collection.fetch()

  onClosePopup: (view, event) ->
    @ui.popup.addClass 'closed'

  onRender: ->
    @showChildView 'sparePartForm', new SparePartApp.BookingSparePartsView
      parent: @
    @showChildView 'sparePartAdd', new SparePartApp.SparePartAddView
      parent: @
    @showChildView 'popup', new SparePartApp.SparePartsView {parent: @}
    @showChildView 'price', new SparePartApp.SparePartPriceView {parent: @}

  initialize: (options) ->
    @listenTo @, 'open:popup', @onOpenPopup
    @listenTo @, 'close:popup', @onClosePopup



class SparePartApp.SparePartPriceView extends Marionette.View
  ###
  Вью для общей цены
  ###
  tagName: 'tr'
  template: _.template """
  <td class="col-title" colspan="2">Сумма за запчасти:</td>
  <td class="col-price"><%- toPrice(price) %></td>
  <td class="col-action"></td>
  """

  templateContext: ->
    price: @price

  onChangePrice: (@price) ->
    if not @price
      @price = 0
    @trigger 'change:price'
    @render()

  initialize: (options) ->
    @price = 0
    @rootView = options.parent
    bookingCollectionView = @rootView.getChildView 'sparePartForm'
    @listenTo bookingCollectionView, 'change:price', @onChangePrice



class SparePartApp.SparePartAddView extends Marionette.View
  ###
  Добавление новой запчасти
  ###
  tagName: 'tr'

  template: _.template """
  <td colspan="3">
    <button class="add-button" type="button" title="Выбрать из списка">
      <i class="fa fa-list-alt"></i> Выбрать
    </button>
  </td>
  """

  ui:
    add: '.add-button'

  events:
    'click @ui.add': 'addSparePart'

  addSparePart: ->
    @rootView.trigger 'open:popup'

  initialize: (options) ->
    @rootView = options.parent



class SparePartApp.BookingSparePartView extends Marionette.View
  ###
  Вью для запчасти заявки
  ###
  className: 'row'
  tagName: 'tr'

  template: _.template """
  <td class="col-title"><%= title %></td>
  <td class="col-guarantee"><%= guarantee ? guarantee.title : '-' %></td>
  <td class="col-price"><%- toPrice(retail_price) %></td>
  <td class="col-action">
    <button class="delete-button" type="button" title="Удалить">
      <i class="fa fa-close"></i>
    </button>
  </td>
  """

  ui:
    delete: '.delete-button'

  triggers:
    'click @ui.delete': 'delete:item'

  onDeleteItem: (view, event) ->
    @model.destroy()

  initialize: (options) ->
    @collectionView = options.parent



class SparePartApp.BookingSparePartsView extends Marionette.CollectionView
  ###
  Вью для всех запчастей заявки
  ###
  childView: SparePartApp.BookingSparePartView
  collection: bookingSpareParts
  tagName: 'tbody'

  childViewOptions: ->
    parent: @

  collectionEvents:
    sync: ->
      @render()
    update: ->
      @trigger 'change:price', @calcPrice()

  calcPrice: ->
    prices = _.compact @collection.pluck 'retail_price'
    _.reduce prices,
      (memo, num) ->
        memo + parseInt(num)
      0

  initialize: (options) ->
    @rootView = options.parent



class SparePartApp.SparePartView extends Marionette.View
  ###
  Вью запчасти доступной для выбора
  ###
  className: 'row'
  tagName: 'tr'

  template: _.template """
  <td class="col-title"><%= title %></td>
  <td class="col-guarantee"><%= guarantee ? guarantee.title : '-' %></td>
  <td class="col-count"><%= count %></td>
  <td class="col-price"><%- toPrice(retail_price) %></td>
  """

  ui:
    el: '.col-title, .col-count, .col-guarantee, .col-price'

  triggers:
    'click @ui.el': 'select:item'

  onSelectItem: (view, event) ->
    booking_el = $ '[data-booking-id]'
    bookingId = booking_el.data 'bookingId'
    @model.save {booking: bookingId}, {success: (model, response) ->
      bookingSpareParts.fetch()
    }

  initialize: (options) ->
    @collectionView = options.parent



class SparePartApp.SparePartsView extends Marionette.CollectionView
  ###
  Вью для всех доступных заявок
  ###
  childView: SparePartApp.SparePartView
  collection: spareParts
  tagName: 'tbody'

  childViewOptions: ->
    parent: @

  collectionEvents:
    sync: ->
      @render()

  childViewEvents:
    'select:item': 'itemSelect'

  itemSelect: (childView) ->
    @rootView.trigger 'close:popup'

  initialize: (options) ->
    @rootView = options.parent
