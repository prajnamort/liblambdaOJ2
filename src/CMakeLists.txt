add_library(lambdaOJ2 SHARED compile.c run_task.c)
install(TARGETS lambdaOJ2 LIBRARY DESTINATION lib)

add_executable(judge judge.c)
target_link_libraries(judge lambdaOJ2)
install(TARGETS judge RUNTIME DESTINATION bin)
