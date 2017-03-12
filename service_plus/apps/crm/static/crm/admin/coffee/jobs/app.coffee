class JobsApp extends Marionette.Application
  region: '#jobs'

  onStart: ->
    @showView new JobsApp.RootView()
    jobs.fetch()
