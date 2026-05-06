require 'open3'

module Jekyll
  class BuildStatsGenerator < Generator
    safe true
    priority :low

    def generate(site)
      js_path  = File.join(site.source, 'assets/js/game.js')
      css_path = File.join(site.source, 'assets/css/main.css')

      site.config['build_js_kb']  = format('%.1f', File.size(js_path)  / 1024.0) if File.exist?(js_path)
      site.config['build_css_kb'] = format('%.1f', File.size(css_path) / 1024.0) if File.exist?(css_path)

      stdout, _, status = Open3.capture3('git rev-parse --short HEAD')
      site.config['build_sha'] = stdout.strip if status.success?
    end
  end
end
