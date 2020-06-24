const dashboard = [
  {
    label: "Dashboard",
    path: "/",
    category: "Dashboard",
  },
];

const auth = [
  {
    label: "Login",
    path: "/login/?next=/admin/login",
    category: "Auth",
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
    path: "/password_change/",
    category: "Auth",
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
    label: "Auth models",
    path: "/auth/",
    category: "Auth",
  },
];

const groups = [
  {
    label: "Groups list",
    path: "/auth/group/",
    category: "Groups",
  },
  {
    label: "Add group",
    path: "/auth/group/add/",
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
    path: "/auth/user/",
    category: "Users",
    states: [
      {
        label: "Search no results",
        path: "/auth/user/?q=test",
      },
      {
        label: "Filtered",
        path: "/auth/user/?is_staff__exact=1",
      },
    ],
  },
  {
    label: "Add user",
    path: "/auth/user/add/",
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
    path: "/polls/",
    category: "Polls",
  },
  {
    label: "Questions list",
    path: "/polls/question/",
    category: "Polls",
  },
  {
    label: "Add question",
    path: "/polls/question/add/",
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

const scenarios = [...dashboard, ...auth, ...groups, ...users, ...polls];

module.exports = scenarios;
