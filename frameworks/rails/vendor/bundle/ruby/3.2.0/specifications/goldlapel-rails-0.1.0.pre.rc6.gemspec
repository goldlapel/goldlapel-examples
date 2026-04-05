# -*- encoding: utf-8 -*-
# stub: goldlapel-rails 0.1.0.pre.rc6 ruby lib

Gem::Specification.new do |s|
  s.name = "goldlapel-rails".freeze
  s.version = "0.1.0.pre.rc6"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.metadata = { "homepage_uri" => "https://goldlapel.com", "source_code_uri" => "https://github.com/goldlapel/goldlapel-rails" } if s.respond_to? :metadata=
  s.require_paths = ["lib".freeze]
  s.authors = ["Stephen Gibson".freeze]
  s.date = "2026-03-21"
  s.description = "Auto-patches ActiveRecord's PostgreSQL adapter to route queries through the Gold Lapel proxy. Zero config \u2014 just add the gem.".freeze
  s.homepage = "https://goldlapel.com".freeze
  s.licenses = ["Proprietary".freeze]
  s.required_ruby_version = Gem::Requirement.new(">= 3.2.0".freeze)
  s.rubygems_version = "3.4.20".freeze
  s.summary = "Gold Lapel integration for Rails".freeze

  s.installed_by_version = "3.4.20" if s.respond_to? :installed_by_version

  s.specification_version = 4

  s.add_runtime_dependency(%q<goldlapel>.freeze, [">= 0"])
  s.add_runtime_dependency(%q<activerecord>.freeze, [">= 7.0"])
  s.add_runtime_dependency(%q<railties>.freeze, [">= 7.0"])
end
