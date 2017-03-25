toPrice = (value) ->
  price = value.toString().replace /\B(?=(\d{3})+(?!\d))/g, ' '
  "#{price} р."



class JobsApp extends Marionette.Application
  region: '#jobs'

  onStart: ->
    window.jobRootView = new JobsApp.RootView()
    @showView window.jobRootView
    jobs.fetch()
