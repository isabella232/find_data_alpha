apt-get update
apt-get install -qy  python3-dev python-virtualenv

mkdir -p /usr/lib/finding
chown -R vagrant /usr/lib/finding/
virtualenv -p /usr/bin/python3 /usr/lib/finding
source /usr/lib/finding/bin/activate


cd /vagrant
pip3 install -r requirements.txt
export DJANGO_SETTINGS_MODULE="find_data.settings.dev"
cd src

# Uncomment if you want to retrieve govuk_template instead of using the included one
#mkdir -p assets
#cd assets
#GOVUK_TEMPLATE_VERSION=0.19.1
#curl -kL "https://github.com/alphagov/govuk_template/releases/download/v${GOVUK_TEMPLATE_VERSION}/django_govuk_template-${GOVUK_TEMPLATE_VERSION}.tgz" | tar xz ./govuk_template

# uncomment if you want to compile govuk_elements yourself instead of using the included one
# Need a recent version of node. Linux distros can be a little late
cd /vagrant
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -

# to compile the SCSS
npm install govuk-elements-sass gulp gulp-sass
gulp styles

