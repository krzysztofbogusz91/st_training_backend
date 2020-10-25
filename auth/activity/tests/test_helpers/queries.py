
activity_query = '''
  query {
    activities {
      id
      activityType,
      startDate,
      name,
      description,
      postedBy {
        username
      },
      cardio {
        duration,
        startDate,
        endDate,
        cardioType
      },
      sections {
        id
        sectionName,
        exercises {
          id
          exerciseName
          sets {
            id
            weights,
            reps,
            notes
          }
        }
      }
    }
  }
'''

token_auth_query = '''
  mutation {
    tokenAuth(username: "jacob", password: "top_secret") {
    token
      payload
      refreshExpiresIn
      refreshToken
    }
  }
'''