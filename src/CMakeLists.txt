add_library(lambdaOJ2 SHARED compile.c run_task.c)
install(TARGETS lambdaOJ2 LIBRARY DESTINATION lib)
