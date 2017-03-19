toPrice = (value) ->
  price = value.toString().replace /\B(?=(\d{3})+(?!\d))/g, ' '
  "#{price} р."



class JobsApp extends Marionette.Application
  region: '#jobs'

  onStart: ->
    @showView new JobsApp.RootView()
    jobs.fetch()
