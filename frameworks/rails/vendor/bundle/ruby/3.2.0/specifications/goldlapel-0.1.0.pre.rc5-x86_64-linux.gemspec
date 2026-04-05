# -*- encoding: utf-8 -*-
# stub: goldlapel 0.1.0.pre.rc5 x86_64-linux lib

Gem::Specification.new do |s|
  s.name = "goldlapel".freeze
  s.version = "0.1.0.pre.rc5"
  s.platform = "x86_64-linux".freeze

  s.required_rubygems_version = Gem::Requirement.new("> 1.3.1".freeze) if s.respond_to? :required_rubygems_version=
  s.metadata = { "homepage_uri" => "https://goldlapel.com", "source_code_uri" => "https://github.com/goldlapel/goldlapel-ruby" } if s.respond_to? :metadata=
  s.require_paths = ["lib".freeze]
  s.authors = ["Stephen Gibson".freeze]
  s.bindir = "exe".freeze
  s.date = "2026-03-19"
  s.description = "Gold Lapel sits between your app and Postgres, watches query patterns, and automatically creates materialized views and indexes to make your database faster. Zero code changes required.".freeze
  s.executables = ["goldlapel".freeze]
  s.files = ["exe/goldlapel".freeze]
  s.homepage = "https://goldlapel.com".freeze
  s.licenses = ["Proprietary".freeze]
  s.required_ruby_version = Gem::Requirement.new(">= 3.2.0".freeze)
  s.rubygems_version = "3.4.20".freeze
  s.summary = "Self-optimizing Postgres proxy \u2014 automatic materialized views and indexes".freeze

  s.installed_by_version = "3.4.20" if s.respond_to? :installed_by_version
end
