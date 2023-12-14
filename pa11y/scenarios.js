const welcome = [
  {
    label: "Welcome",
    path: "/debug/default_urlconf/",
    category: "Welcome",
  },
];

const errors = [
  {
    label: "404",
    path: "/defaults/404/",
    category: "Errors",
  },
  {
    label: "500",
    path: "/defaults/500/",
    category: "Errors",
  },
  {
    label: "403",
    path: "/defaults/403/",
    category: "Errors",
  },
  {
    label: "400",
    path: "/defaults/400/",
    category: "Errors",
  },
  {
    label: "CSRF",
    path: "/defaults/csrf_failure/",
    category: "Errors",
  },
];

const static = [
  {
    label: "Directory index",
    path: "/defaults/directory_index/",
    category: "Static",
  },
];

const dashboard = [
  {
    label: "Dashboard",
    path: "/admin/",
    category: "Dashboard",
  },
];

const auth = [
  {
    label: "Login",
    path: "/admin/login/?next=/admin/login",
    category: "Auth",
    skip: "Unreliable due to expiring password reset token",
    unauthenticated: true,
    states: [
      {
        label: "Validation error",
        actions: [
          "set field #id_username to test_123456",
          "set field #id_password to doesnotexist",
          'click element [type="submit"]',
          "wait for element .errornote to be visible",
        ],
      },
    ],
  },
  {
    label: "Password change",
    path: "/admin/password_change/",
    category: "Auth",
    skip: "Unreliable due to expiring password reset token",
    states: [
      {
        label: "Validation error",
        actions: [
          "set field #id_old_password to test_123456",
          "set field #id_new_password1 to doesnotexist",
          "set field #id_new_password2 to potato",
          'click element [type="submit"]',
          "wait for element .errornote to be visible",
        ],
      },
    ],
  },
  {
    label: "Password reset",
    path: "/admin/password_reset/",
    category: "Auth",
    unauthenticated: true,
  },
  {
    label: "Password reset done",
    path: "/admin/password_reset/done/",
    category: "Auth",
    unauthenticated: true,
  },
  {
    label: "Password reset confirm",
    path: "/reset/MQ/a6x18q-2816d310e4da13869c0c5e1f15774cb8/",
    category: "Auth",
    unauthenticated: true,
    skip: "Unreliable due to expiring password reset token",
    states: [
      {
        label: "Validation error",
        actions: [
          "set field #id_new_password1 to doesnotexist",
          "set field #id_new_password2 to potato",
          'click element [type="submit"]',
          "wait for element .errorlist to be visible",
        ],
      },
    ],
  },
  {
    label: "Password reset confirm unsuccessful",
    path: "/reset/MQ/set-password/",
    category: "Auth",
    unauthenticated: true,
  },
  {
    label: "Password reset complete",
    path: "/reset/done/",
    category: "Auth",
    unauthenticated: true,
  },
  {
    label: "Auth models",
    path: "/admin/auth/",
    category: "Auth",
  },
];

const groups = [
  {
    label: "Groups list",
    path: "/admin/auth/group/",
    category: "Groups",
  },
  {
    label: "Add group",
    path: "/admin/auth/group/add/",
    category: "Groups",
    states: [
      {
        label: "Validation error",
        actions: [
          'click element [type="submit"]',
          "wait for element .errornote to be visible",
        ],
      },
    ],
  },
  {
    label: "Add group popup",
    path: "/admin/auth/group/add/?_to_field=id&_popup=1",
    category: "Groups",
    states: [
      {
        label: "Validation error",
        actions: [
          'click element [type="submit"]',
          "wait for element .errornote to be visible",
        ],
      },
    ],
  },
];

const users = [
  {
    label: "Users list",
    path: "/admin/auth/user/",
    category: "Users",
    states: [
      {
        label: "Search no results",
        path: "/admin/auth/user/?q=test",
      },
      {
        label: "Filtered",
        path: "/admin/auth/user/?is_staff__exact=1",
      },
    ],
  },
  {
    label: "Edit user",
    path: "/admin/auth/user/1/change/",
    category: "Users",
  },
  {
    label: "Edit user success",
    path: "/admin/auth/user/1/change/",
    category: "Users",
    actions: [
      'click element [type="submit"]',
      "wait for element .success to be visible",
    ],
  },
  {
    label: "Delete user confirm",
    path: "/admin/auth/user/1/delete/",
    category: "Users",
  },
  {
    label: "Change history",
    path: "/admin/auth/user/1/history/",
    category: "Users",
    states: [],
  },
  {
    label: "Add user",
    path: "/admin/auth/user/add/",
    category: "Users",
    states: [
      {
        label: "Validation error",
        actions: [
          'click element [type="submit"]',
          "wait for element .errornote to be visible",
        ],
      },
    ],
  },
];

const polls = [
  {
    label: "Polls models",
    path: "/admin/polls/",
    category: "Polls",
  },
  {
    label: "Questions list",
    path: "/admin/polls/question/",
    category: "Polls",
  },
  {
    label: "Add question",
    path: "/admin/polls/question/add/",
    category: "Polls",
    states: [
      {
        label: "Validation error",
        actions: [
          'click element [type="submit"]',
          "wait for element .errornote to be visible",
        ],
      },
      {
        label: "Datepicker",
        actions: [
          "click element #calendarlink0",
          "wait for element #calendarbox0 to be visible",
        ],
      },
      {
        label: "Timepicker",
        actions: [
          "click element #clocklink0",
          "wait for element #clockbox0 to be visible",
        ],
      },
    ],
  },
];

const admindocs = [
  {
    label: "Docs index",
    path: "/admin/doc/",
    category: "admindocs",
  },
  {
    label: "Tags",
    path: "/admin/doc/tags/",
    category: "admindocs",
  },
  {
    label: "Filters",
    path: "/admin/doc/filters/",
    category: "admindocs",
  },
  {
    label: "Views",
    path: "/admin/doc/views/",
    category: "admindocs",
  },
  {
    label: "Bookmarklets",
    path: "/admin/doc/bookmarklets/",
    category: "admindocs",
  },
  {
    label: "Models",
    path: "/admin/doc/models/",
    category: "admindocs",
  },
  {
    label: "Models – admin.LogEntry",
    path: "/admin/doc/models/admin.logentry/",
    category: "admindocs",
  },
  {
    label: "Models – auth.Permission",
    path: "/admin/doc/models/auth.permission/",
    category: "admindocs",
  },
  {
    label: "Models – auth.Group",
    path: "/admin/doc/models/auth.group/",
    category: "admindocs",
  },
  {
    label: "Models – auth.User",
    path: "/admin/doc/models/auth.user/",
    category: "admindocs",
  },
  {
    label: "Models – contenttypes.ContentType",
    path: "/admin/doc/models/contenttypes.contenttype/",
    category: "admindocs",
  },
  {
    label: "Models – sessions.Session",
    path: "/admin/doc/models/sessions.session/",
    category: "admindocs",
  },
  {
    label: "Models – sites.Site",
    path: "/admin/doc/models/sites.site/",
    category: "admindocs",
  },
  {
    label: "Models – flatpages.FlatPage",
    path: "/admin/doc/models/flatpages.flatpage/",
    category: "admindocs",
  },
];

const flatpages = [
  {
    label: "Flatpages list",
    path: "/admin/flatpages/flatpage/",
    category: "Flatpages",
  },
  {
    label: "Add flatpage",
    path: "/admin/flatpages/flatpage/add/",
    category: "Flatpages",
    states: [
      {
        label: "Validation error",
        actions: [
          'click element [type="submit"]',
          "wait for element .errornote to be visible",
        ],
      },
      {
        label: "Advanced options",
        actions: ["click element #fieldsetcollapser0"],
      },
    ],
  },
];

const sites = [
  {
    label: "Sites list",
    path: "/admin/sites/site/",
    category: "Sites",
  },
  {
    label: "Edit site",
    path: "/admin/sites/site/1/change/",
    category: "Sites",
  },
  {
    label: "Edit site success",
    path: "/admin/sites/site/1/change/",
    category: "Sites",
    actions: [
      'click element [type="submit"]',
      "wait for element .success to be visible",
    ],
  },
  {
    label: "Delete site confirm",
    path: "/admin/sites/site/1/delete/",
    category: "Sites",
  },
  {
    label: "Change history",
    path: "/admin/sites/site/1/history/",
    category: "Sites",
    states: [],
  },
  {
    label: "Add site",
    path: "/admin/sites/site/add/",
    category: "Sites",
    states: [
      {
        label: "Validation error",
        actions: [
          'click element [type="submit"]',
          "wait for element .errornote to be visible",
        ],
      },
    ],
  },
];

const scenarios = [
  welcome,
  errors,
  static,
  dashboard,
  auth,
  groups,
  users,
  polls,
  admindocs,
  flatpages,
  sites,
].flat();

module.exports = scenarios;
