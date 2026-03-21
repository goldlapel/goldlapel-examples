require "rails"
require "active_model/railtie"
require "active_record/railtie"
require "action_controller/railtie"

module TodoApp
  class Application < Rails::Application
    config.load_defaults 7.1
    config.api_only = true
  end
end
