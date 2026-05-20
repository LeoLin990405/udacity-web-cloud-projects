package com.udacity.project4.locationreminders.reminderslist

import android.app.Application
import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import androidx.test.core.app.ApplicationProvider
import com.udacity.project4.locationreminders.data.FakeDataSource
import com.udacity.project4.locationreminders.data.dto.ReminderDTO
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.TestCoroutineDispatcher
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.setMain
import org.hamcrest.CoreMatchers.`is`
import org.hamcrest.MatcherAssert.assertThat
import org.junit.After
import org.junit.Before
import org.junit.Rule
import org.junit.Test

@ExperimentalCoroutinesApi
class RemindersListViewModelTest {
    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    private val testDispatcher = TestCoroutineDispatcher()
    private lateinit var dataSource: FakeDataSource
    private lateinit var viewModel: RemindersListViewModel

    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        dataSource = FakeDataSource()
        viewModel = RemindersListViewModel(
            ApplicationProvider.getApplicationContext<Application>(),
            dataSource
        )
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
        testDispatcher.cleanupTestCoroutines()
    }

    @Test
    fun loadReminders_withData_populatesReminderListAndHidesNoData() {
        dataSource.addReminders(
            ReminderDTO("Title", "Description", "Location", 1.0, 2.0, "id-1")
        )

        viewModel.loadReminders()

        assertThat(viewModel.remindersList.value?.size, `is`(1))
        assertThat(viewModel.showNoData.value, `is`(false))
    }

    @Test
    fun loadReminders_withoutData_showsNoData() {
        viewModel.loadReminders()

        assertThat(viewModel.remindersList.value?.isEmpty(), `is`(true))
        assertThat(viewModel.showNoData.value, `is`(true))
    }
}
