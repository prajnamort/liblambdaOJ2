add_library(lambdaOJ2 STATIC compile.c run_task.c)

add_executable(judge judge.c)
target_link_libraries(judge lambdaOJ2)
install(TARGETS judge RUNTIME DESTINATION bin)

add_executable(compile_code compile_code.c)
target_link_libraries(compile_code lambdaOJ2)
install(TARGETS compile_code RUNTIME DESTINATION bin)
