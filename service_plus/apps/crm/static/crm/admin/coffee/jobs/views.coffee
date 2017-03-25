class JobsApp.AvailableJobView extends Marionette.View
  className: 'row'
  tagName: 'tr'

  template: _.template """
  <td class="col-title"><%= title %></td>
  <td class="col-price"><%- toPrice(price) %></td>
  """

  ui:
    job: '.col-title, .col-price'

  triggers:
    'click @ui.job': 'select:item'



class JobsApp.AvailableJobsView extends Marionette.CollectionView
  childView: JobsApp.AvailableJobView
  collection: availableJobs
  tagName: 'table'


  childViewEvents:
    'select:item': 'itemSelect'

  itemSelect: (childView) ->
    model = @rootView._model
    model.set
      title: childView.model.get 'title'
      price: childView.model.get 'price'
    @rootView.trigger 'close:popup'

  initialize: (options) ->
    @rootView = options.parent


class JobsApp.JobView extends Marionette.View
  className: 'row'
  tagName: 'tr'

  template: _.template """
  <td class="col-title">
    <input class="title-input" type="text" name="title" value="<%= title %>">
  </td>

  <td class="col-price">
    <input class="price-input" type="text" name="price" value="<%= price %>">
  </td>

  <td class="col-action">
    <button class="choose-button" type="button" title="Выбрать из списка">
      <i class="fa fa-list-alt"></i>
    </button>
    <button class="delete-button" type="button" title="Удалить">
      <i class="fa fa-close"></i>
    </button>
  </td>
  """

  ui:
    choose: '.choose-button'
    delete: '.delete-button'
    price: '.price-input'
    title: '.title-input'

  modelEvents:
    'change': 'render'

  events:
    'change input': 'changed'

  triggers:
    'click @ui.choose': 'choose:item'
    'click @ui.delete': 'delete:item'

  changed: (event) ->
    @model.set
      title: @ui.title.val()
      price: @ui.price.val()

  initialize: (options) ->
    _.bindAll @, 'changed'
    @collectionView = options.parent



class JobsApp.JobsView extends Marionette.CollectionView
  childView: JobsApp.JobView
  collection: jobs
  tagName: 'tbody'

  childViewOptions: ->
    parent: @

  childViewEvents:
    'choose:item': 'itemChoose'
    'delete:item': 'itemDelete'

  collectionEvents:
    'add': 'actOnChange'
    'change': 'actOnChange'
    'remove': 'actOnChange'

  actOnChange: (model) ->
    objs = @collection.map (obj) ->
      obj = obj.toJSON()
      if obj.title
        obj
    prices = _.compact _.pluck objs, 'price'
    fullPrice = _.reduce prices,
      (memo, num) ->
        memo + parseInt(num)
      0
    @collection.save()
    @trigger 'price', fullPrice

  itemChoose: (childView) ->
    availableJobs.fetch()
    @rootView.trigger 'open:popup', childView

  itemDelete: (childView) ->
    childView.model.destroy()

  initialize: (options) ->
    @rootView = options.parent



class JobsApp.JobsAddView extends Marionette.View
  tagName: 'tr'

  template: _.template """
  <td colspan="3">
    <button class="add-button" type="button" title="Добавить новую запись">
      <i class="fa fa-plus"></i> Добавить
    </button>
  </td>
  """

  events:
    'click @ui.add': 'addJob'

  ui:
    add: '.add-button'

  addJob: ->
    @collectionView.collection.create()

  initialize: (options) ->
    @collectionView = options.parent.getChildView 'jobsForm'



class JobsApp.JobsPriceView extends Marionette.View
  tagName: 'tr'
  template: _.template """
  <td class="col-title">Сумма за ремонт:</td>
  <td class="col-price"><%- toPrice(price) %></td>
  <td class="col-action"></td>
  """

  templateContext: ->
    price: @price

  onPrice: (@price) ->
    @trigger 'change:price'
    @render()

  initialize: (options) ->
    @price = 0
    @collectionView = options.parent.getChildView 'jobsForm'
    @listenTo @collectionView, 'price', @onPrice



class JobsApp.RootView extends Marionette.View
  template: _.template """
  <table id="jobs-form">
    <thead>
      <tr>
        <th>Работа</th>
        <th>Цена</th>
        <th></th>
      </tr>
    </thead>
    <tbody></tbody>
    <tfoot>
      <tr id="jobs-form-add"></tr>
      <tr id="jobs-price"></tr>
    </tfoot>
  </table>
  <div id="jobs-popup" class="closed">
    <div id="available-jobs"></div>
    <div class="overlay"></div>
  </div>
  """

  ui:
    popup: '#jobs-popup'
    overlay: '#jobs-popup .overlay'

  events:
    'click @ui.popup': 'closePopup'

  closePopup: (event) ->
    if event.target is @ui.overlay[0]
      @trigger 'close:popup'

  onOpenPopup: (view, event) ->
    @ui.popup.removeClass 'closed'
    @_model = view.model

  onClosePopup: (view, event) ->
    @ui.popup.addClass 'closed'
    @_model = null

  regions:
    jobsForm:
      el: 'tbody'
      replaceElement: true
    jobsFormAdd:
      el: '#jobs-form-add'
      replaceElement: true
    jobsFullPrice:
      el: '#jobs-price'
      replaceElement: true
    jobsPopup:
      el: '#available-jobs'

  onRender: ->
    @showChildView 'jobsForm', new JobsApp.JobsView {parent: @}
    @showChildView 'jobsFormAdd', new JobsApp.JobsAddView {parent: @}
    @showChildView 'jobsFullPrice', new JobsApp.JobsPriceView {parent: @}
    @showChildView 'jobsPopup', new JobsApp.AvailableJobsView {parent: @}

  initialize: (options) ->
    @listenTo @, 'open:popup', @onOpenPopup
    @listenTo @, 'close:popup', @onClosePopup
