require 'test/unit'
require "yaml"

class TestCoordinateValidation < Test::Unit::TestCase

  def test_coordinatevalidation
    Dir["./_pins/*.json"].each do |path|
      f = YAML.load_file(path) #rescue raise(path)
      [
        f["latitude"],
        f["longitude"],
      ].all? do |s|
        s.to_s[/^-?\d+\.\d+$/]
      end
    end

  end
end
