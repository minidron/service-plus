class JobsApp.AvailableJob extends Backbone.Model
  defaults:
    title: ''
    price: 0



class JobsApp.AvailableJobs extends Backbone.Collection
  model: JobsApp.AvailableJob
  url: '/api/jobs'

availableJobs = new JobsApp.AvailableJobs()



class JobsApp.Job extends Backbone.Model
  defaults:
    title: ''
    price: 0

  # Чтобы не было ошибки из-за отсутствия URL
  sync: ->
    null



class JobsApp.Jobs extends Backbone.Collection
  model: JobsApp.Job

  fetch: ->
    objs = @getObjects()
    if typeof objs is 'string'
      objs = JSON.parse objs

    _.each objs, (obj) =>
      @create
        title: obj.title
        price: obj.price

  save: ->
    objs = @map (obj) ->
      obj = obj.toJSON()
      if obj.title
        obj
    clearObjs = _.compact objs
    if clearObjs.length
      val = clearObjs
    else
      val = null
    $(@field).val JSON.stringify val

  getObjects: ->
    objs = $(@field).val()
    if objs is 'null'
      {}
    else
      objs

  initialize: (options) ->
    @field = '#id_done_work'

jobs = new JobsApp.Jobs()
